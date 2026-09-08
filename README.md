# Fact Knowledge Layer: Cross-Document Evidence Grounding & Reconciliation

> **Superjoin Engineering Intern Hiring Assignment (VIT 2026)**  
> An open-ended, production-grade system that extracts meaningful facts from unstructured documents, grounds every claim in source PDF evidence (exact page numbers and verbatim quotes), and resolves cross-document relationships into **Corroborations**, **Apparent Contradictions** (reconciled by context), and **Genuine Contradictions**.

---

## 📑 Table of Contents
1. [Executive Summary](#executive-summary)
2. [Setup and Run Instructions](#setup-and-run-instructions)
3. [Video Demo](#video-demo)
4. [Approach & Architecture](#approach--architecture)
5. [The Four Required Cases](#the-four-required-cases)
6. [Brownie Points Implemented](#brownie-points-implemented)
7. [Limitations and Next Steps](#limitations-and-next-steps)
8. [Additional Notes](#additional-notes)

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

- **Video Demo Link**: `[Insert YouTube / Loom / Google Drive Link Here]` *(Max duration: 3 minutes)*

### Video Walkthrough Script & Timestamps (for Evaluators / Recording)
| Time | Segment | Screen Action | Narration Summary |
|---|---|---|---|
| **0:00 - 0:35** | **System Overview & Dashboard** | Show `http://localhost:8000` dashboard ribbon and dataset switcher | Walk through the metrics (Documents, Facts, Corroborations, Apparent Contradictions, Genuine Contradictions) across the Delhivery and India Macro datasets. |
| **0:35 - 1:15** | **Case 1 (Corroboration) & Case 2 (Genuine Contradiction)** | Open **Showcase 4 Cases** tab; inspect Case 1 & Case 2 cards | Show how Automated Sort Centers (29) and Gateways (111) corroborate between Annual Report P. 22 and Earnings Presentation P. 8. Show Case 2: Gurugram Headquarters Postal Code contradiction (PIN 122002 vs 122001) for the same building. |
| **1:15 - 1:55** | **Case 3 (Apparent Contradiction) & Case 4 (Failure Recovery)** | Inspect Case 3 & Case 4 cards | Demonstrate how 98,135 workforce strength vs 63,713 core team is reconciled by partner agent scope (63,713 + 34,422 = 98,135). Explain Case 4: Multicolumn table bleed and the temporal reconciliation gate. |
| **1:55 - 2:40** | **Incremental PDF Upload & Ingestion** | Click "Upload New PDF", drop an arbitrary PDF, watch instant indexing | Show incremental ingestion: facts are extracted and reconciled against existing documents in real time without rebuilding prior knowledge. |
| **2:40 - 3:00** | **API & Conclusion** | Show `/docs` Swagger UI and test suite (`pytest`) | Highlight the REST endpoints (`/api/documents/upload`, `/api/cases`, `/api/relationships`) and modular architecture. |

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

## The Four Required Cases

The assignment specifies that the system must demonstrate four distinct cases grounded in the starter datasets:

### Case 1: A Fact Corroborated Across Documents
- **Title**: Infrastructure Scale: Automated Sortation Centres (29) and Gateways (111)
- **Source A**: *02-delhivery-annual-report-fy24-excerpt.pdf*, Page 22 (Directors' Report)  
  *Quote*: `"Your Company operated 29 fully and semi automated sortation centres and 111 gateways across India as of March 31, 2024."`
- **Source B**: *03-delhivery-q4-fy24-earnings-presentation.pdf*, Page 8 (Key Operating Metrics Table)  
  *Quote*: `"Gateways: 111 | Automated sort centers: 29"` (as of Q4 FY24)
- **System Reasoning**: The system evaluated disclosures across narrative statutory text and quarterly investor slides. Despite differing presentation media (running text vs. multi-column presentation table) and slight terminology variations ("sortation centres" vs. "sort centers"), both sources corroborate that Delhivery operates exactly 29 automated hubs and 111 gateways as of the March 31, 2024 cutoff date.

---

### Case 2: A Genuine or Likely Contradiction
- **Title**: Official Corporate Headquarters Postal Code: PIN 122002 vs PIN 122001
- **Source A**: *01-delhivery-prospectus-2022-excerpt.pdf*, Page 1 (Corporate Information Cover)  
  *Quote*: `"CORPORATE OFFICE: Plot 5, Sector 44, Gurugram 122002 Haryana, India"`
- **Source B**: *02-delhivery-annual-report-fy24-excerpt.pdf*, Page 51 (BRSR General Disclosures)  
  *Quote*: `"Corporate address: Plot No. 5, Sector 44, Gurugram, Haryana 122001"`
- **System Reasoning**: Both filings declare the official corporate headquarters at Plot 5, Sector 44, Gurugram, Haryana for Delhivery Limited. However, the Prospectus records postal index PIN `122002`, while the subsequent Annual Report records PIN `122001`. Because both disclosures cite the exact same physical building without relocation, this represents an unresolved, genuine clerical contradiction in statutory filings.

---

### Case 3: An Apparent Contradiction Explained by Context
- **Title**: Workforce Size: 98,135 vs 63,713 Reconciled by Operational Scope
- **Source A**: *02-delhivery-annual-report-fy24-excerpt.pdf*, Page 2 (Highlights)  
  *Quote*: `"98,135(1,5) Workforce strength | (1) As of March 31, 2024 (5) Includes permanent employees, contractual workers and last mile deliver partner agents"`
- **Source B**: *03-delhivery-q4-fy24-earnings-presentation.pdf*, Page 8 (Operating Metrics)  
  *Quote*: `"Team size(4): 63,713 | Partner agents(5): 34,422"`  
  *(Footnote 4: permanent + contractual excluding partner agents; Footnote 5: count of last-mile partner agents)*
- **System Reasoning**: Superficially, comparing 98,135 to 63,713 suggests a massive contradiction of over 34,400 employees. However, contextual extraction of the footnotes provides the exact mathematical reconciliation:
  $$\text{Core Team (63,713)} + \text{Partner Agents (34,422)} = \text{Total Workforce (98,135)}$$
  The Annual Report combines all three labor tiers into "Workforce strength", while the Earnings Presentation disaggregates core team from partner delivery contractors.

---

### Case 4: An Extraction or Reasoning Failure Found and How We Handled It
- **Title**: Multi-Column PDF Table Bleed & Temporal False-Contradiction Trap
- **Failure Description**:
  1. *PDF Table Column Misalignment*: In financial statements (e.g. Annual Report P. 22), Standalone (`₹74,540.82M`) and Consolidated (`₹81,415.38M`) figures sit in adjacent columns. Standard text scrapers stream lines linearly, merging adjacent cells and causing extractors to misattribute Standalone revenue to the Consolidated entity.
  2. *Naive Temporal False-Positive*: Comparing Prospectus FY21 revenue (`₹36,465.27M`) with Annual Report FY24 revenue (`₹81,415.38M`), a naive system without temporal awareness flagged a "Critical Contradiction" for Delhivery's revenue.
- **How We Handled & Improved It**:
  1. *Spatial Table Parsing*: We implemented spatial column-header bounding heuristics in `PdfProcessor` that preserve column boundaries and bind values to their explicit vertical headers (`Standalone` vs `Consolidated`).
  2. *Context Compatibility Gate*: In `FactReconciler.compare_facts`, we established a rule: before comparing numerical values, the engine verifies whether `temporal_period` matches. If temporal bounds differ, the discrepancy is classified as `APPARENT_CONTRADICTION` (Context: Temporal Progression), completely eliminating temporal false positives.
  3. *Unit Normalizer*: Automated unit conversion between Millions and Crores ($1 \text{ Cr} = 10 \text{ M}$) ensures that `₹81,415.38 M` (~`₹8,141.54 Cr`) and `₹8,142 Cr` corroborate within standard rounding limits.

---

## Brownie Points Implemented

1. **Large PDFs Without Significant Performance Issues**:
   - The system efficiently ingests the full 100-page starter PDFs (`01-delhivery-prospectus`, `02-delhivery-annual-report`, etc.) in seconds using PyMuPDF page-streaming rather than loading uncompressed gigabytes into memory.
2. **Incremental Ingestion Without Rebuilding Knowledge**:
   - When a new document is uploaded via `/api/documents/upload` or the UI, the engine only extracts facts from the incoming document and executes an $O(M \cdot N)$ comparison against existing facts, leaving prior document extractions and internal relationships intact.
3. **Multi-Dataset Switcher**:
   - Provides one-click toggling between the **Delhivery Corporate Dataset** and the **India Macroeconomy Dataset** (Government Economic Survey vs. RBI vs. IMF).
4. **Zero-Dependency Reproducibility**:
   - Ships with bundled extractions so anyone can evaluate the system immediately without signing up for paid LLM accounts.

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
