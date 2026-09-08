"""
FastAPI application for the Fact Knowledge Layer system.
Provides REST API endpoints and serves the interactive UI.
"""

import os
import shutil
import logging
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.core.models import Fact, Relationship, DocumentMetadata, CaseStudy
from app.core.store import store

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Fact Knowledge Layer API",
    description="Extracts, grounds, and reconciles facts across documents with contextual reasoning.",
    version="1.0.0"
)

# Enable CORS for local testing / development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


class LoadDatasetRequest(BaseModel):
    dataset: str  # "delhivery", "india-macroeconomy", or "all"


@app.get("/api/status")
def get_system_status() -> Dict[str, Any]:
    """Get system summary metrics for dashboard ribbons."""
    return store.get_stats()


@app.get("/api/documents", response_model=List[DocumentMetadata])
def get_documents() -> List[DocumentMetadata]:
    """List all currently indexed documents."""
    return store.get_documents()


@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Incrementally upload and process a new PDF document:
    Extracts facts from this document and reconciles them against existing facts.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        doc_meta, new_facts, new_rels = store.add_document_incremental(
            file_path=file_path,
            filename=file.filename
        )

        return {
            "message": f"Successfully processed '{file.filename}' incrementally.",
            "document": doc_meta,
            "facts_extracted": len(new_facts),
            "new_relationships_formed": len(new_rels),
            "stats": store.get_stats()
        }
    except Exception as e:
        logger.exception("Error processing uploaded PDF")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.get("/api/facts", response_model=List[Fact])
def get_facts(
    entity: Optional[str] = Query(None, description="Filter by entity name"),
    category: Optional[str] = Query(None, description="Filter by category"),
    document_id: Optional[str] = Query(None, description="Filter by source document ID"),
    q: Optional[str] = Query(None, description="Keyword search query")
) -> List[Fact]:
    """Search and filter extracted facts."""
    return store.get_facts(entity=entity, category=category, document_id=document_id, search_query=q)


@app.get("/api/relationships", response_model=List[Relationship])
def get_relationships(
    type: Optional[str] = Query(None, description="Filter by type (CORROBORATED, APPARENT_CONTRADICTION, GENUINE_CONTRADICTION)"),
    entity: Optional[str] = Query(None, description="Filter by entity name")
) -> List[Relationship]:
    """Retrieve cross-document relationships with contextual reasoning."""
    return store.get_relationships(rel_type=type, entity=entity)


@app.get("/api/cases", response_model=List[CaseStudy])
def get_evaluation_cases() -> List[CaseStudy]:
    """Retrieve the four required evaluation cases with full source grounding."""
    return store.get_cases()


@app.post("/api/dataset/load")
def switch_dataset(req: LoadDatasetRequest) -> Dict[str, Any]:
    """Switch active knowledge dataset (delhivery, india-macroeconomy, or all)."""
    valid_datasets = ["delhivery", "india-macroeconomy", "all"]
    if req.dataset not in valid_datasets:
        raise HTTPException(status_code=400, detail=f"Invalid dataset. Choose from {valid_datasets}")

    store.load_dataset(req.dataset)
    return {
        "message": f"Switched dataset to '{req.dataset}'",
        "stats": store.get_stats()
    }


@app.post("/api/reconcile")
def trigger_reconciliation() -> Dict[str, Any]:
    """Re-run pairwise cross-document reconciliation."""
    store.reconcile_all()
    return {
        "message": "Reconciliation recomputed successfully.",
        "stats": store.get_stats()
    }


# Static files and UI routes
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def serve_ui():
    """Serve the single-page application."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Fact Knowledge Layer API is running. Frontend index.html not yet placed."}
