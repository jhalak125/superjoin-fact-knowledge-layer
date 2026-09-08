"""
Core data models for the Fact Knowledge Layer system.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid


class RelationshipType(str, Enum):
    CORROBORATED = "CORROBORATED"
    APPARENT_CONTRADICTION = "APPARENT_CONTRADICTION"
    GENUINE_CONTRADICTION = "GENUINE_CONTRADICTION"
    RELATED = "RELATED"


class ContextFactor(str, Enum):
    TEMPORAL = "TEMPORAL"          # Different time period / reporting year / effective date
    SCOPE = "SCOPE"                # Standalone vs Consolidated, Core Team vs Total Workforce
    UNIT = "UNIT"                  # Crore vs Million vs Count vs Percentage
    METHODOLOGY = "METHODOLOGY"    # Accounting standard (Ind AS vs IFRS), Pro forma vs Restated
    VINTAGE = "VINTAGE"            # First Advance Estimates vs Revised / Provisional Estimates
    LEGAL_STATUS = "LEGAL_STATUS"  # Pre-IPO Unlisted (U) vs Post-IPO Listed (L)


class Evidence(BaseModel):
    """Grounded evidence linking a fact back to its exact source document location."""
    document_id: str
    document_name: str
    page_number: int = Field(description="1-indexed page number in the source PDF")
    quote: str = Field(description="Exact verbatim excerpt from the document")
    surrounding_context: Optional[str] = Field(default=None, description="Broader paragraph or section context")
    section_title: Optional[str] = Field(default=None, description="Section or table header")
    char_offset: Optional[int] = Field(default=None, description="Character start offset on page if available")


class FactContext(BaseModel):
    """Contextual qualifiers that disambiguate what a fact represents."""
    temporal_period: Optional[str] = Field(default=None, description="e.g. FY24, Q4 FY24, March 31, 2024, FY2024-25")
    scope: Optional[str] = Field(default=None, description="e.g. Consolidated, Standalone, Pan-India, Core Employees")
    unit: Optional[str] = Field(default=None, description="e.g. INR Million, INR Crore, %, Number, Address")
    accounting_or_source_note: Optional[str] = Field(default=None, description="e.g. Pro forma, Ind AS, MoSPI, NSO")


class Fact(BaseModel):
    """An extracted atomic numerical or semantic fact."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    entity: str = Field(description="The primary subject entity (e.g., Delhivery Limited, Indian Economy)")
    attribute: str = Field(description="The property or metric (e.g., Revenue from operations, PIN codes covered)")
    value: str = Field(description="Original stated value (e.g., ₹81,415.38 million, 18,793, 6.5%)")
    normalized_value: Optional[float] = Field(default=None, description="Parsed numeric value in standard units if applicable")
    normalized_unit: Optional[str] = Field(default=None, description="Standardized unit (e.g. INR_CR, COUNT, PERCENT)")
    category: str = Field(default="General", description="Category: Financial, Operational, Governance, Macroeconomic")
    context: FactContext = Field(default_factory=FactContext)
    evidence: Evidence
    confidence: float = Field(default=0.95, ge=0.0, le=1.0)


class Relationship(BaseModel):
    """A cross-document relationship between two facts with reasoning."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    fact_a_id: str
    fact_b_id: str
    relationship_type: RelationshipType
    reconciling_factors: List[ContextFactor] = Field(default_factory=list)
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)
    reasoning: str = Field(description="Detailed natural language chain of reasoning explaining the relationship")
    comparison_summary: str = Field(description="Short human-readable summary of comparison")
    
    # Hydrated fact copies for easier API consumption
    fact_a: Optional[Fact] = None
    fact_b: Optional[Fact] = None


class CaseStudy(BaseModel):
    """Showcase evaluation case demonstrating the 4 required scenarios."""
    case_number: int
    case_type: str = Field(description="e.g. Corroborated, Genuine Contradiction, Apparent Contradiction, Failure")
    title: str
    description: str
    fact_a: Optional[Fact] = None
    fact_b: Optional[Fact] = None
    evidence_a: Optional[Evidence] = None
    evidence_b: Optional[Evidence] = None
    system_reasoning: str
    handling_or_improvement: Optional[str] = None
    technical_takeaway: str


class DocumentMetadata(BaseModel):
    """Metadata for an uploaded or indexed PDF document."""
    id: str
    filename: str
    title: str
    total_pages: int
    dataset_group: Optional[str] = "custom"
    file_size_bytes: int
    facts_count: int = 0
    indexed_at: str
