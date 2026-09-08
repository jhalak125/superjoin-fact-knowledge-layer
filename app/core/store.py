"""
Fact Knowledge Store.
Maintains grounded facts, relationships, and metadata with incremental document ingestion.
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from app.core.models import Fact, Relationship, DocumentMetadata, CaseStudy, RelationshipType
from app.core.reconciler import FactReconciler
from app.core.cases import get_showcase_cases
from app.core.datasets import (
    get_delhivery_documents,
    get_delhivery_facts,
    get_macro_documents,
    get_macro_facts
)
from app.core.extractor import FactExtractor

logger = logging.getLogger(__name__)


class KnowledgeStore:
    """In-memory and JSON-backed Fact Knowledge Store with incremental indexing."""

    def __init__(self):
        self.documents: Dict[str, DocumentMetadata] = {}
        self.facts: Dict[str, Fact] = {}
        self.relationships: List[Relationship] = []
        self.active_dataset: str = "delhivery"
        self.cases: List[CaseStudy] = get_showcase_cases()
        
        # Load default dataset
        self.load_dataset("delhivery")

    def load_dataset(self, dataset_name: str) -> None:
        """Switch or reset to a specific starter dataset or load all."""
        self.documents.clear()
        self.facts.clear()
        self.relationships.clear()
        self.active_dataset = dataset_name

        if dataset_name == "delhivery":
            for doc in get_delhivery_documents():
                self.documents[doc.id] = doc
            for f in get_delhivery_facts():
                self.facts[f.id] = f
        elif dataset_name == "india-macroeconomy":
            for doc in get_macro_documents():
                self.documents[doc.id] = doc
            for f in get_macro_facts():
                self.facts[f.id] = f
        elif dataset_name == "all":
            for doc in get_delhivery_documents() + get_macro_documents():
                self.documents[doc.id] = doc
            for f in get_delhivery_facts() + get_macro_facts():
                self.facts[f.id] = f

        # Run reconciliation on all loaded facts
        self.reconcile_all()

    def reconcile_all(self) -> None:
        """Re-reconcile all facts currently in the store."""
        fact_list = list(self.facts.values())
        self.relationships = FactReconciler.reconcile_all(fact_list)

    def add_document_incremental(self, file_path: str, filename: str) -> Tuple[DocumentMetadata, List[Fact], List[Relationship]]:
        """
        Incrementally ingest a new PDF:
        1. Parse and extract facts from this document ONLY.
        2. Reconcile newly extracted facts against existing store facts (O(M * N) instead of full rebuild).
        """
        import uuid
        doc_id = f"doc-custom-{str(uuid.uuid4())[:6]}"
        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        
        import pymupdf
        try:
            doc = pymupdf.open(file_path)
            total_pages = len(doc)
        except Exception:
            total_pages = 1

        doc_meta = DocumentMetadata(
            id=doc_id,
            filename=filename,
            title=filename.replace(".pdf", "").replace("-", " ").title(),
            total_pages=total_pages,
            dataset_group="uploaded",
            file_size_bytes=file_size,
            facts_count=0,
            indexed_at=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.documents[doc_id] = doc_meta

        # Extract facts from the new document
        extractor = FactExtractor(doc_id=doc_id, doc_name=filename, pdf_path=file_path)
        new_facts = extractor.extract_all_facts()

        if not new_facts:
            # Fallback heuristic: create high-level overview fact
            new_facts.append(Fact(
                entity="Uploaded Document Entity",
                attribute="Document Overview",
                value=f"Processed document containing {total_pages} pages.",
                category="General",
                evidence=Evidence(
                    document_id=doc_id,
                    document_name=filename,
                    page_number=1,
                    quote=f"Document: {filename}",
                    surrounding_context=f"Ingested {filename} with {total_pages} pages."
                ),
                confidence=0.85
            ))

        # Add new facts to store
        for f in new_facts:
            self.facts[f.id] = f
        doc_meta.facts_count = len(new_facts)

        # Incremental reconciliation: compare new facts against existing facts ONLY
        existing_facts = [f for f in self.facts.values() if f.evidence.document_id != doc_id]
        new_relationships = []
        for nf in new_facts:
            for ef in existing_facts:
                rel = FactReconciler.compare_facts(nf, ef)
                if rel:
                    new_relationships.append(rel)
                    self.relationships.append(rel)

        return doc_meta, new_facts, new_relationships

    def get_stats(self) -> Dict[str, Any]:
        """Return system statistics for the dashboard ribbon."""
        total_docs = len(self.documents)
        total_facts = len(self.facts)
        
        corroborated_count = sum(1 for r in self.relationships if r.relationship_type == RelationshipType.CORROBORATED)
        apparent_count = sum(1 for r in self.relationships if r.relationship_type == RelationshipType.APPARENT_CONTRADICTION)
        genuine_count = sum(1 for r in self.relationships if r.relationship_type == RelationshipType.GENUINE_CONTRADICTION)

        return {
            "active_dataset": self.active_dataset,
            "total_documents": total_docs,
            "total_facts": total_facts,
            "corroborated_relationships": corroborated_count,
            "apparent_contradictions": apparent_count,
            "genuine_contradictions": genuine_count,
            "total_relationships": len(self.relationships)
        }

    def get_facts(
        self,
        entity: Optional[str] = None,
        category: Optional[str] = None,
        document_id: Optional[str] = None,
        search_query: Optional[str] = None
    ) -> List[Fact]:
        """Search and filter extracted facts."""
        results = list(self.facts.values())

        if entity:
            results = [f for f in results if entity.lower() in f.entity.lower()]
        if category:
            results = [f for f in results if category.lower() in f.category.lower()]
        if document_id:
            results = [f for f in results if f.evidence.document_id == document_id]
        if search_query:
            q = search_query.lower()
            results = [
                f for f in results
                if q in f.entity.lower()
                or q in f.attribute.lower()
                or q in f.value.lower()
                or q in f.evidence.quote.lower()
            ]

        return results

    def get_relationships(
        self,
        rel_type: Optional[str] = None,
        entity: Optional[str] = None
    ) -> List[Relationship]:
        """Retrieve cross-document relationships with optional filters."""
        results = self.relationships

        if rel_type:
            target = rel_type.upper()
            results = [r for r in results if r.relationship_type.value == target]
        if entity:
            e = entity.lower()
            results = [
                r for r in results
                if (r.fact_a and e in r.fact_a.entity.lower()) or (r.fact_b and e in r.fact_b.entity.lower())
            ]

        return results

    def get_documents(self) -> List[DocumentMetadata]:
        return list(self.documents.values())

    def get_cases(self) -> List[CaseStudy]:
        return self.cases


# Global singleton instance for the app
store = KnowledgeStore()
