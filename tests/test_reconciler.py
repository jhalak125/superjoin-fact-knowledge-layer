"""
Unit tests for cross-document reconciliation logic.
Tests corroboration, apparent contradiction, and genuine contradiction.
"""

import pytest
from app.core.models import Fact, Evidence, FactContext, RelationshipType, ContextFactor
from app.core.reconciler import FactReconciler


def test_corroboration_exact_match():
    fact_a = Fact(
        id="fa",
        entity="Delhivery Limited",
        attribute="Automated Sort Centers",
        value="29 automated sort centres",
        normalized_value=29.0,
        context=FactContext(temporal_period="March 31, 2024"),
        evidence=Evidence(document_id="doc1", document_name="doc1.pdf", page_number=22, quote="29 sort centres")
    )
    fact_b = Fact(
        id="fb",
        entity="Delhivery Limited",
        attribute="Automated Sort Centers",
        value="29 automated sort centres",
        normalized_value=29.0,
        context=FactContext(temporal_period="March 31, 2024"),
        evidence=Evidence(document_id="doc2", document_name="doc2.pdf", page_number=8, quote="29 automated sort centers")
    )

    rel = FactReconciler.compare_facts(fact_a, fact_b)
    assert rel is not None
    assert rel.relationship_type == RelationshipType.CORROBORATED
    assert "Direct corroboration" in rel.comparison_summary or "matching value" in rel.reasoning


def test_corroboration_revenue_unit_conversion():
    # Annual Report ₹81,415.38 M (~8,141.54 Cr) vs Presentation ₹8,142 Cr
    fact_a = Fact(
        id="rev-m",
        entity="Delhivery Limited",
        attribute="Revenue from operations",
        value="₹81,415.38 million",
        normalized_value=8141.54,
        context=FactContext(temporal_period="FY 2023-24 (Full Year)", scope="Consolidated", unit="INR Million"),
        evidence=Evidence(document_id="doc1", document_name="ar24.pdf", page_number=22, quote="Revenue: 81,415.38")
    )
    fact_b = Fact(
        id="rev-cr",
        entity="Delhivery Limited",
        attribute="Revenue from services",
        value="₹8,142 Cr",
        normalized_value=8142.0,
        context=FactContext(temporal_period="FY 2023-24 (Full Year)", scope="Consolidated Services", unit="INR Crore"),
        evidence=Evidence(document_id="doc2", document_name="ep24.pdf", page_number=6, quote="₹8,142 Cr")
    )

    rel = FactReconciler.compare_facts(fact_a, fact_b)
    assert rel is not None
    assert rel.relationship_type == RelationshipType.CORROBORATED
    assert ContextFactor.UNIT in rel.reconciling_factors


def test_apparent_contradiction_workforce_scope():
    # Total workforce 98,135 (including partner agents) vs Core team 63,713
    fact_a = Fact(
        id="wf",
        entity="Delhivery Limited",
        attribute="Workforce Strength",
        value="98,135 personnel",
        normalized_value=98135.0,
        context=FactContext(temporal_period="March 31, 2024", scope="Total Workforce"),
        evidence=Evidence(document_id="doc1", document_name="ar24.pdf", page_number=2, quote="98,135 Workforce strength")
    )
    fact_b = Fact(
        id="ts",
        entity="Delhivery Limited",
        attribute="Team Size",
        value="63,713 employees",
        normalized_value=63713.0,
        context=FactContext(temporal_period="March 31, 2024", scope="Core Team"),
        evidence=Evidence(document_id="doc2", document_name="ep24.pdf", page_number=8, quote="Team size: 63,713")
    )

    rel = FactReconciler.compare_facts(fact_a, fact_b)
    assert rel is not None
    assert rel.relationship_type == RelationshipType.APPARENT_CONTRADICTION
    assert ContextFactor.SCOPE in rel.reconciling_factors
    assert "partner agent" in rel.reasoning.lower()


def test_apparent_contradiction_pre_post_ipo_cin():
    # Prospectus U63090... vs Annual Report L63090...
    fact_a = Fact(
        id="cin-u",
        entity="Delhivery Limited",
        attribute="Corporate Identity Number (CIN)",
        value="U63090DL2011PLC221234",
        context=FactContext(temporal_period="Pre-IPO"),
        evidence=Evidence(document_id="doc1", document_name="prospectus.pdf", page_number=1, quote="CIN: U63090DL2011PLC221234")
    )
    fact_b = Fact(
        id="cin-l",
        entity="Delhivery Limited",
        attribute="Corporate Identity Number (CIN)",
        value="L63090DL2011PLC221234",
        context=FactContext(temporal_period="Post-IPO"),
        evidence=Evidence(document_id="doc2", document_name="ar24.pdf", page_number=51, quote="CIN: L63090DL2011PLC221234")
    )

    rel = FactReconciler.compare_facts(fact_a, fact_b)
    assert rel is not None
    assert rel.relationship_type == RelationshipType.APPARENT_CONTRADICTION
    assert ContextFactor.LEGAL_STATUS in rel.reconciling_factors


def test_genuine_contradiction_gurugram_pin_code():
    # Prospectus 122002 vs Annual Report 122001 for Plot 5, Sector 44
    fact_a = Fact(
        id="addr-02",
        entity="Delhivery Limited",
        attribute="Corporate Headquarters Postal PIN Code",
        value="Plot 5, Sector 44, Gurugram 122002 Haryana, India",
        context=FactContext(scope="Corporate Headquarters"),
        evidence=Evidence(document_id="doc1", document_name="prospectus.pdf", page_number=1, quote="Gurugram 122002")
    )
    fact_b = Fact(
        id="addr-01",
        entity="Delhivery Limited",
        attribute="Corporate Headquarters Postal PIN Code",
        value="Plot No. 5, Sector 44, Gurugram, Haryana 122001",
        context=FactContext(scope="Corporate Headquarters"),
        evidence=Evidence(document_id="doc2", document_name="ar24.pdf", page_number=51, quote="Gurugram 122001")
    )

    rel = FactReconciler.compare_facts(fact_a, fact_b)
    assert rel is not None
    assert rel.relationship_type == RelationshipType.GENUINE_CONTRADICTION
    assert "122002 vs 122001" in rel.comparison_summary
