# Fact Knowledge Layer: Cross-Document Evidence Grounding & Reconciliation

> **Superjoin Engineering Intern Hiring Assignment**  
> An open-ended, production-grade system that extracts meaningful facts from unstructured documents, grounds every claim in source PDF evidence (exact page numbers and verbatim quotes), and resolves cross-document relationships into **Corroborations**, **Apparent Contradictions** (reconciled by context), and **Genuine Contradictions**.

---

## 📑 Table of Contents
1. [Executive Summary](#executive-summary)
2. [Setup and Run Instructions](#setup-and-run-instructions)
3. [Video Demo](#video-demo)
4. [Approach & Architecture](#approach--architecture)
5. [Limitations and Next Steps](#limitations-and-next-steps)
6. [Additional Notes](#additional-notes)

---

## Executive Summary

Important facts are scattered across corporate filings, financial disclosures, and institutional reports. A simple vector database or naive LLM prompt fails when comparing such facts:
- Stated values often disagree not because one is false, but because their **contextual dimensions** differ (e.g., **time periods**, **reporting scope** such as Standalone vs. Consolidated, **measurement units**, or **data vintages**).
- Naive retrieval systems hallucinate contradictions across fiscal years (e.g., calling FY21 revenue vs. FY24 revenue a "critical contradiction") or miss genuine errors hidden in footnotes.

The **Fact Knowledge Layer** solves this by establishing a multi-dimensional factual schema where every fact is bound to:
1. **Verifiable Grounding**: Exact PDF page number, verbatim excerpt, and surrounding context.
2. **Contextual Metadata**: Temporal span, organizational scope, units, and accounting standards.
3. **Cross-Document Reconciliation Engine**: Automated pairwise comparison that classifies relationships into `CORROBORATED`, `APPARENT_CONTRADICTION`, or `GENUINE_CONTRADICTION`, outputting a natural language chain of reasoning.

---

## Setup and Run Instructions

The system is designed to run **zero-config out-of-the-box** without requiring paid API credentials or external database servers.

### 1. Prerequisites
- **Python 3.10+**
- macOS, Linux, or Windows (WSL recommended)

### 2. Quickstart (One Command)
Clone the repository and set up the environment:

```bash
# Clone the repository
git clone <your-repo-url>
cd "Superjoin Assignment"

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Launch the Application
Run the runner script:
```bash
python run.py
```
Or run directly via Uvicorn:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser and navigate to:
- **Interactive UI**: `http://localhost:8000`
- **Interactive OpenAPI Docs (Swagger)**: `http://localhost:8000/docs`

### 4. Running the Automated Test Suite
Run the 16 unit tests covering extraction, models, reconciliation logic, and API endpoints:
```bash
pytest -v
```

---

## Video Demo

<p align="center">
  <a href="https://drive.google.com/file/d/1jcMpm0L3Q9P2kAAJ_J2hSIn4s6rzivoB/view?usp=sharing">
    <br>
    ▶️ <b>Click here to watch the full video demo</b>
  </a>
</p>



---

## Approach & Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       FastAPI Server                        │
│   GET /api/status   GET /api/cases   POST /api/upload      │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
               ▼                               ▼
    ┌────────────────────┐          ┌──────────────────────┐
    │ Layout-Aware PDF   │          │  Knowledge Store     │
    │ Processor (fitz)   │          │  - Facts Catalog     │
    │ - Text extraction  │          │  - Evidence Grounding│
    │ - Table alignment  │          │  - Document Metas    │
    │ - Quote grounding  │          └──────────┬───────────┘
    └──────────┬─────────┘                     │
               │                               │
               ▼                               ▼
    ┌────────────────────┐          ┌──────────────────────┐
    │  Fact Extractor    │          │  Cross-Document      │
    │  - Semantic nodes  │─────────▶│  Reconciler Engine   │
    │  - Context tagging │          │  - Compatibility gate│
    │  - Normalizer      │          │  - Unit conversion   │
    └────────────────────┘          │  - Reasoning chain   │
                                    └──────────────────────┘
```

### 1. The Fact Data Model
A fact is not merely a `(subject, predicate, object)` triple; it requires grounded provenance and multidimensional context:
- **`Entity`**: The subject (e.g., `Delhivery Limited`, `Indian Economy`).
- **`Attribute`**: The metric (e.g., `Revenue from Operations`, `Workforce Strength`, `CIN`).
- **`Value`**: Original stated value (e.g., `₹81,415.38 million`, `98,135 personnel`, `6.5%`).
- **`Normalized Value & Unit`**: Standardized numerical representation (e.g., `8141.54 INR_CR`, `98135 COUNT`, `6.5 PERCENT`).
- **`Context Qualifiers`**:
  - `temporal_period`: `FY 2023-24`, `Q4 FY24`, `Pre-IPO`, `March 31, 2024`.
  - `scope`: `Consolidated`, `Standalone`, `Core Team`, `Total Workforce`.
  - `unit`: `INR Million`, `INR Crore`, `Personnel Count`.
  - `accounting_or_source_note`: `Ind AS`, `Pro forma`, `NSO Advance Estimates`.
- **`Evidence Grounding`**: Source document ID, document filename, 1-indexed page number, and verbatim quotation.

### 2. Layout-Aware PDF Ingestion (`app/core/extractor.py`)
PDF extraction often scrambles multi-column tables. Using `pymupdf` (`fitz`), our processor preserves reading order and spatial blocks. It verifies that extracted quotes exist verbatim on the cited page.

### 3. Cross-Document Reconciliation Engine (`app/core/reconciler.py`)
When comparing facts from Document A and Document B:
1. **Entity & Metric Compatibility**: Establishes whether both facts refer to compatible underlying real-world concepts.
2. **Unit Normalization**: Automatically converts between scale multiples (e.g. ₹ Million to ₹ Crore: $81,415.38 \text{ M} \div 10 = 8,141.54 \text{ Cr} \approx 8,142 \text{ Cr}$).
3. **Context Compatibility Gate**:
   - If temporal bounds differ (e.g., FY21 vs FY24, or Pre-IPO vs Post-IPO), the system routes to `APPARENT_CONTRADICTION` with `ContextFactor.TEMPORAL` or `ContextFactor.LEGAL_STATUS`.
   - If operational boundaries differ (e.g., Total Workforce vs Core Team), it flags `ContextFactor.SCOPE`.
   - If context matches and normalized values match within rounding tolerance $\to$ `CORROBORATED`.
   - If context matches but values conflict without explanation $\to$ `GENUINE_CONTRADICTION`.

---

## Limitations and Next Steps

### Current Limitations
1. **Scanned Images / Non-OCR PDFs**:
   - The current pipeline relies on text-layer extraction via PyMuPDF. Purely image-scanned PDFs without embedded text require an upstream OCR engine (e.g., Tesseract or Google Cloud Vision).
2. **Complex Merged Cells & Multi-Tier Tables**:
   - While two-tier headers are handled, deeply nested multi-row header tables with spanning cells occasionally require manual verification.

### Next Steps & Future Enhancements
1. **Vector Embedding Hybrids for Semantic Predicate Matching**:
   - Augment the rule-based attribute alias map with dense embedding cosine similarity (e.g., `sentence-transformers`) for open-domain predicate clustering across thousands of arbitrary documents.
2. **Interactive Graph Visualization**:
   - Add a 2D interactive force-directed node graph (e.g., using Cytoscape.js or D3.js) to visually trace provenance chains.
3. **Pluggable Local LLM Integration**:
   - Enable direct one-click hookup to local Ollama instances (`llama3`, `mistral`) for zero-data-leakage enterprise environments.

---

## Additional Notes

- **AI Tools Used**: Developed with the assistance of Google Antigravity paired with PyMuPDF, FastAPI, and Pytest.
- **Repository Cleanliness**: No credentials or private API keys are tracked in the repository. Sample datasets and test fixtures are self-contained.
- **Form Submission**: Submitted alongside the GitHub repository link and demo video through the official hiring form.
