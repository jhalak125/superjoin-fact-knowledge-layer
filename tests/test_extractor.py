"""
Unit tests for PDFProcessor and quote grounding verification.
"""

import os
import pytest
from app.core.extractor import PDFProcessor


def test_quote_verification_prospectus():
    pdf_path = "starter-datasets/delhivery/01-delhivery-prospectus-2022-excerpt.pdf"
    if not os.path.exists(pdf_path):
        pytest.skip("Starter dataset PDF not found")

    # Verify CIN quote on page 1
    found, quote = PDFProcessor.verify_quote(
        pdf_path=pdf_path,
        page_number=1,
        quote="CORPORATE IDENTITY NUMBER: U63090DL2011PLC221234"
    )
    assert found is True


def test_quote_verification_annual_report():
    pdf_path = "starter-datasets/delhivery/02-delhivery-annual-report-fy24-excerpt.pdf"
    if not os.path.exists(pdf_path):
        pytest.skip("Starter dataset PDF not found")

    # Verify Pin codes covered quote on page 2
    found, quote = PDFProcessor.verify_quote(
        pdf_path=pdf_path,
        page_number=2,
        quote="18,793"
    )
    assert found is True


def test_quote_verification_earnings_presentation():
    pdf_path = "starter-datasets/delhivery/03-delhivery-q4-fy24-earnings-presentation.pdf"
    if not os.path.exists(pdf_path):
        pytest.skip("Starter dataset PDF not found")

    # Verify ₹8,142 Cr revenue quote on page 6
    found, quote = PDFProcessor.verify_quote(
        pdf_path=pdf_path,
        page_number=6,
        quote="₹8,142 Cr"
    )
    assert found is True
