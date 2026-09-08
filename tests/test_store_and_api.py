"""
Unit tests for KnowledgeStore and FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.store import store

client = TestClient(app)


def test_get_status():
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert "total_documents" in data
    assert "total_facts" in data
    assert "corroborated_relationships" in data
    assert data["total_documents"] >= 3


def test_get_documents():
    response = client.get("/api/documents")
    assert response.status_code == 200
    docs = response.json()
    assert len(docs) >= 3
    assert any("delhivery" in d["filename"].lower() for d in docs)


def test_get_facts_and_filtering():
    response = client.get("/api/facts")
    assert response.status_code == 200
    facts = response.json()
    assert len(facts) > 0

    # Filter by category
    gov_res = client.get("/api/facts?category=Governance")
    assert gov_res.status_code == 200
    gov_facts = gov_res.json()
    assert all(f["category"] == "Governance" for f in gov_facts)


def test_get_relationships():
    response = client.get("/api/relationships")
    assert response.status_code == 200
    rels = response.json()
    assert len(rels) > 0

    # Filter by type
    corrob_res = client.get("/api/relationships?type=CORROBORATED")
    assert corrob_res.status_code == 200
    corrob_rels = corrob_res.json()
    assert all(r["relationship_type"] == "CORROBORATED" for r in corrob_rels)


def test_get_showcase_cases():
    response = client.get("/api/cases")
    assert response.status_code == 200
    cases = response.json()
    assert len(cases) == 4
    
    case_types = [c["case_type"] for c in cases]
    assert "CORROBORATED" in case_types
    assert "GENUINE_CONTRADICTION" in case_types
    assert "APPARENT_CONTRADICTION" in case_types
    assert "EXTRACTION_REASONING_FAILURE" in case_types


def test_switch_dataset():
    response = client.post("/api/dataset/load", json={"dataset": "india-macroeconomy"})
    assert response.status_code == 200
    data = response.json()
    assert data["stats"]["active_dataset"] == "india-macroeconomy"

    # Switch back to delhivery
    back_res = client.post("/api/dataset/load", json={"dataset": "delhivery"})
    assert back_res.status_code == 200
    assert back_res.json()["stats"]["active_dataset"] == "delhivery"
