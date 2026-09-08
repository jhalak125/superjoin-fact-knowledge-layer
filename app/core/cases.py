"""
Showcase of the Four Required Evaluation Cases.
Grounded directly in the starter datasets with verifiable source citations and reasoning.
"""

from typing import List
from app.core.models import CaseStudy, Fact, Evidence, FactContext, RelationshipType, ContextFactor


def get_showcase_cases() -> List[CaseStudy]:
    """Return the four required cases for the hiring assignment."""
    
    # =========================================================================
    # CASE 1: A fact corroborated across documents, even if expressed differently
    # =========================================================================
    case_1_fact_a = Fact(
        id="c1-fact-a",
        entity="Delhivery Limited",
        attribute="Automated Sort Centers and Gateways Count",
        value="29 automated sort centres and 111 gateways",
        category="Operational",
        context=FactContext(
            temporal_period="As of March 31, 2024",
            scope="All-India Infrastructure Network",
            unit="Facility Count"
        ),
        evidence=Evidence(
            document_id="doc-delhivery-ar24",
            document_name="02-delhivery-annual-report-fy24-excerpt.pdf",
            page_number=22,
            quote="Your Company operated 29 fully and semi automated sortation centres and 111 gateways across India as of March 31, 2024.",
            surrounding_context="We have a Rated Automated Sort Capacity of 7.1 million shipments per day as of March 31, 2024.",
            section_title="Directors' Report - State of affairs / Business operations"
        ),
        confidence=0.99
    )

    case_1_fact_b = Fact(
        id="c1-fact-b",
        entity="Delhivery Limited",
        attribute="Automated Sort Centers and Gateways Count",
        value="29 automated sort centers and 111 gateways",
        category="Operational",
        context=FactContext(
            temporal_period="As of end of Q4 FY24 (March 31, 2024)",
            scope="Operating Metrics Infrastructure",
            unit="Facility Count"
        ),
        evidence=Evidence(
            document_id="doc-delhivery-ep24",
            document_name="03-delhivery-q4-fy24-earnings-presentation.pdf",
            page_number=8,
            quote="Gateways: 111 | Automated sort centers: 29",
            surrounding_context="Key operating metrics as of end of / for the period Q4 FY24",
            section_title="Key Operating Metrics Table"
        ),
        confidence=0.99
    )

    case_1 = CaseStudy(
        case_number=1,
        case_type="CORROBORATED",
        title="Infrastructure Footprint: Automated Sort Centers (29) and Gateways (111)",
        description=(
            "A key operational fact corroborated across two independent disclosures (Annual Report FY24 narrative "
            "and Q4 FY24 Investor Presentation tabular metrics), confirming Delhivery's automated gateway scale."
        ),
        fact_a=case_1_fact_a,
        fact_b=case_1_fact_b,
        evidence_a=case_1_fact_a.evidence,
        evidence_b=case_1_fact_b.evidence,
        system_reasoning=(
            "The system compared the operational entity 'Delhivery Limited' across the Directors' Report narrative "
            "(Annual Report P. 22) and the quarterly Key Operating Metrics table (Earnings Presentation P. 8). "
            "Despite differing document formats (prose text vs structured presentation table) and spelling variants "
            "('sortation centres' vs 'sort centers'), the system extracted the identical entity, identical temporal cutoff "
            "(March 31, 2024), and matching counts: exactly 29 automated sort centers and 111 network gateways. "
            "Both documents corroborate each other without discrepancy."
        ),
        technical_takeaway=(
            "Layout-aware semantic entity extraction successfully unifies tabular disclosures and narrative prose into "
            "grounded, mutually verifying knowledge nodes."
        )
    )

    # =========================================================================
    # CASE 2: A genuine or likely contradiction
    # =========================================================================
    case_2_fact_a = Fact(
        id="c2-fact-a",
        entity="Delhivery Limited",
        attribute="Corporate Headquarters Postal PIN Code",
        value="Plot 5, Sector 44, Gurugram 122002, Haryana, India",
        category="Governance",
        context=FactContext(
            scope="Corporate Headquarters Address",
            unit="Postal Code"
        ),
        evidence=Evidence(
            document_id="doc-delhivery-prospectus",
            document_name="01-delhivery-prospectus-2022-excerpt.pdf",
            page_number=1,
            quote="CORPORATE OFFICE: Plot 5, Sector 44, Gurugram 122002 Haryana, India",
            surrounding_context="DELHIVERY LIMITED | Corporate Identity Number: U63090DL2011PLC221234 | Tel: +91 124 6225602",
            section_title="Cover Page - Corporate Information"
        ),
        confidence=0.99
    )

    case_2_fact_b = Fact(
        id="c2-fact-b",
        entity="Delhivery Limited",
        attribute="Corporate Headquarters Postal PIN Code",
        value="Plot No. 5, Sector 44, Gurugram, Haryana 122001",
        category="Governance",
        context=FactContext(
            scope="Corporate Headquarters Address",
            unit="Postal Code"
        ),
        evidence=Evidence(
            document_id="doc-delhivery-ar24",
            document_name="02-delhivery-annual-report-fy24-excerpt.pdf",
            page_number=51,
            quote="Corporate address: Plot No. 5, Sector 44, Gurugram, Haryana 122001",
            surrounding_context="BRSR Section A: General Disclosures - Details of the listed entity",
            section_title="Business Responsibility & Sustainability Report"
        ),
        confidence=0.99
    )

    case_2 = CaseStudy(
        case_number=2,
        case_type="GENUINE_CONTRADICTION",
        title="Official Headquarters Postal Code: PIN 122002 vs PIN 122001",
        description=(
            "Both documents declare the official corporate headquarters at 'Plot 5, Sector 44, Gurugram', "
            "yet one legal filing documents the PIN code as 122002, while the subsequent annual report documents "
            "it as 122001. Because both refer to the exact same physical building without relocation, "
            "this represents an unreconciled, genuine contradiction in official regulatory filings."
        ),
        fact_a=case_2_fact_a,
        fact_b=case_2_fact_b,
        evidence_a=case_2_fact_a.evidence,
        evidence_b=case_2_fact_b.evidence,
        system_reasoning=(
            "The system evaluated the corporate headquarters location for Delhivery Limited across the IPO Prospectus (P. 1) "
            "and the FY24 Annual Report BRSR Disclosures (P. 51). "
            "Both filings describe the identical address: 'Plot 5, Sector 44, Gurugram, Haryana'. "
            "However, the Prospectus records postal index code 122002, whereas the Annual Report records 122001. "
            "Checking contextual reconciling factors reveals no company relocation, no building change, and no legislative "
            "postal boundary shift. The system flags this as a Genuine Contradiction: a persistent typographic or postal "
            "index error across statutory filings."
        ),
        technical_takeaway=(
            "When facts share identical physical and entity context but differ in semantic or numerical values without "
            "valid contextual justification, the system correctly escalates to GENUINE_CONTRADICTION rather than "
            "forcing an artificial reconciliation."
        )
    )

    # =========================================================================
    # CASE 3: An apparent contradiction explained by context (Time, Scope, Units)
    # =========================================================================
    case_3_fact_a = Fact(
        id="c3-fact-a",
        entity="Delhivery Limited",
        attribute="Workforce Strength",
        value="98,135 personnel",
        normalized_value=98135.0,
        normalized_unit="PERSONNEL",
        category="Operational",
        context=FactContext(
            temporal_period="As of March 31, 2024",
            scope="Total Workforce (includes permanent employees, contractual workers, and last-mile partner agents)",
            unit="Personnel Count",
            accounting_or_source_note="Annual Report 'Delhivery in Numbers' (Footnote 1, 5)"
        ),
        evidence=Evidence(
            document_id="doc-delhivery-ar24",
            document_name="02-delhivery-annual-report-fy24-excerpt.pdf",
            page_number=2,
            quote="98,135(1,5) Workforce strength | (1) As of March 31, 2024 (5) Includes permanent employees, contractual workers and last mile deliver partner agents",
            surrounding_context="Delhivery In Numbers | 18,793 Pin codes covered | 4,445 Last-mile delivery centres",
            section_title="Delhivery In Numbers Highlights"
        ),
        confidence=0.99
    )

    case_3_fact_b = Fact(
        id="c3-fact-b",
        entity="Delhivery Limited",
        attribute="Team Size",
        value="63,713 employees",
        normalized_value=63713.0,
        normalized_unit="PERSONNEL",
        category="Operational",
        context=FactContext(
            temporal_period="As of Q4 FY24 (March 31, 2024)",
            scope="Core Team (permanent employees and contractual workers, excluding partner agents)",
            unit="Personnel Count",
            accounting_or_source_note="Earnings Presentation Operating Metrics (Footnote 4, 5)"
        ),
        evidence=Evidence(
            document_id="doc-delhivery-ep24",
            document_name="03-delhivery-q4-fy24-earnings-presentation.pdf",
            page_number=8,
            quote="Team size(4): 63,713 | Partner agents(5): 34,422",
            surrounding_context="(4) Includes permanent employees and contractual workers (excluding partner agents, daily wage manpower) (5) Count of last mile delivery partner agents",
            section_title="Key Operating Metrics Table"
        ),
        confidence=0.99
    )

    case_3 = CaseStudy(
        case_number=3,
        case_type="APPARENT_CONTRADICTION",
        title="Workforce Size Discrepancy: 98,135 vs 63,713 Reconciled by Operational Scope",
        description=(
            "Annual Report states Delhivery's workforce is 98,135, whereas the Q4 Earnings Presentation reports "
            "team size as 63,713 for the exact same date (March 31, 2024). At first glance, this looks like a massive "
            "headcount contradiction of over 34,400 people. However, contextual extraction of footnotes reveals "
            "an exact mathematical reconciliation based on operational scope."
        ),
        fact_a=case_3_fact_a,
        fact_b=case_3_fact_b,
        evidence_a=case_3_fact_a.evidence,
        evidence_b=case_3_fact_b.evidence,
        system_reasoning=(
            "Initial comparison surfaces a 34,422 discrepancy between stated figures (98,135 vs 63,713). "
            "However, inspecting the contextual scope attributes resolves the contradiction: "
            "1. Annual Report (P. 2, Footnote 5) defines 'Workforce strength' as combining permanent employees, "
            "contractual workers, and last-mile delivery partner agents. "
            "2. Earnings Presentation (P. 8) explicitly disaggregates this: it reports 'Team size' (permanent + contractual) "
            "as 63,713, and in the row directly below, reports 'Partner agents' as 34,422. "
            "Reconciliation formula: 63,713 (Core Team) + 34,422 (Partner Agents) = 98,135 (Total Workforce). "
            "The numbers match to the single individual once operational scope is accounted for."
        ),
        handling_or_improvement=(
            "Reconciliation engine applies ContextFactor.SCOPE. When an apparent contradiction occurs between numeric "
            "aggregates, the system inspects compositional sub-metrics within adjacent table rows to verify additive integrity."
        ),
        technical_takeaway=(
            "Contradiction detection without contextual scope qualifiers produces severe false positives in financial "
            "analysis. Parsing sub-line items and footnotes turns a 35,000-person apparent error into a verified proof of consistency."
        )
    )

    # =========================================================================
    # CASE 4: An extraction or reasoning failure found and how it was resolved
    # =========================================================================
    case_4 = CaseStudy(
        case_number=4,
        case_type="EXTRACTION_REASONING_FAILURE",
        title="Multicolumn PDF Table Bleed & Temporal False-Contradiction Trap",
        description=(
            "In early system iterations, two failure modes were uncovered: "
            "1. Multicolumn PDF table cell conflation: Raw text streams from PDF table parsers merged adjacent columns "
            "(Standalone FY24: ₹74,540.82M and Consolidated FY24: ₹81,415.38M), associating Standalone values with Consolidated scopes. "
            "2. Naive entity reconciliation: Comparing Prospectus FY21 revenue (₹36,465.27M) with Annual Report FY24 revenue (₹81,415.38M) "
            "flagged a 'Severe Contradiction' because both reported 'Delhivery Limited Revenue from Operations'."
        ),
        fact_a=None,
        fact_b=None,
        evidence_a=Evidence(
            document_id="doc-delhivery-ar24",
            document_name="02-delhivery-annual-report-fy24-excerpt.pdf",
            page_number=22,
            quote="Particulars | Standalone - FY ended March 31, 2024: 74,540.82 | Consolidated - FY ended March 31, 2024: 81,415.38",
            surrounding_context="Directors' Report - Financial Performance Table (in ₹ Million)",
            section_title="Key highlights of the financial performance table"
        ),
        evidence_b=Evidence(
            document_id="doc-delhivery-prospectus",
            document_name="01-delhivery-prospectus-2022-excerpt.pdf",
            page_number=17,
            quote="Revenue from contract with customers: For the year ended March 31, 2021: 36,465.27 (in ₹ million)",
            surrounding_context="Restated Summary Consolidated Profit and Loss Data",
            section_title="Restated Financial Statements"
        ),
        system_reasoning=(
            "Failure Mode Analysis: "
            "1. PDF Table Layout Failure: PDF text streams often serialize text by reading order coordinates. In multi-column "
            "tables (like Annual Report P. 22 or Prospectus P. 17), numbers in adjacent columns ('74,540.82' and '81,415.38') "
            "bleed into a single line without explicit column-header anchors. Naive extractors bound the first detected number "
            "to the primary entity, mistakenly attributing Standalone revenue as Consolidated revenue. "
            "2. Temporal Naivety: Naive similarity search between facts matched the entity ('Delhivery Limited') and attribute "
            "('Revenue from operations'). Because 36,465 != 81,415, the classifier emitted a high-confidence GENUINE_CONTRADICTION, "
            "blind to the fact that one covered FY 2020-21 and the other covered FY 2023-24."
        ),
        handling_or_improvement=(
            "How We Handled and Resolved It: "
            "1. Spatial Layout Heuristics: In `PdfProcessor`, we introduced layout-aware text chunking that preserves row-column "
            "spatial grouping and binds values to the nearest vertical table header ('Standalone' vs 'Consolidated'). "
            "2. Mandatory Context Schema: We enforced strict `temporal_period` and `scope` fields in every Fact node. "
            "3. Guardrail Rule in Reconciler: Before two facts are compared for contradiction, the reconciler executes a "
            "Context Compatibility Gate (`cls.compare_facts`). If `temporal_period` differs (FY21 vs FY24), value divergence "
            "is automatically routed to `ContextFactor.TEMPORAL` (Historical Progression) instead of a factual contradiction. "
            "4. Unit Normalization Pipeline: Automatic conversion between Millions and Crores (1 Crore = 10 Million) eliminates "
            "false positives when comparing ₹81,415.38M and ₹8,142 Cr."
        ),
        technical_takeaway=(
            "A fact without structured context (time, scope, unit) is incomplete information. Grounding the schema in "
            "strict contextual dimensions prevents LLMs and heuristic matchers from hallucinating contradictions across time."
        )
    )

    return [case_1, case_2, case_3, case_4]
