"""
Unit tests for core data models.
"""

import pytest
from app.core.models import (
    Fact,
    Evidence,
    FactContext,
    Relationship,
    RelationshipType,
    ContextFactor,
    CaseStudy
)


def test_fact_creation_and_grounding():
    evidence = Evidence(
        document_id="doc-1",
        document_name="test.pdf",
        page_number=5,
        quote="Delhivery operates 111 gateways"
    )
    context = FactContext(
        temporal_period="FY24",
        scope="Pan-India",
        unit="Count"
    )
    fact = Fact(
        entity="Delhivery Limited",
        attribute="Gateways Count",
        value="111 gateways",
        normalized_value=111.0,
        normalized_unit="COUNT",
        category="Operational",
        context=context,
        evidence=evidence
    )

    assert fact.entity == "Delhivery Limited"
    assert fact.attribute == "Gateways Count"
    assert fact.normalized_value == 111.0
    assert fact.evidence.page_number == 5
    assert fact.evidence.quote == "Delhivery operates 111 gateways"


def test_relationship_creation():
    rel = Relationship(
        fact_a_id="f1",
        fact_b_id="f2",
        relationship_type=RelationshipType.CORROBORATED,
        reconciling_factors=[ContextFactor.UNIT],
        reasoning="Both values agree once converted to standard currency units.",
        comparison_summary="Revenue figures match."
    )

    assert rel.relationship_type == RelationshipType.CORROBORATED
    assert ContextFactor.UNIT in rel.reconciling_factors
    assert "Revenue" in rel.comparison_summary
