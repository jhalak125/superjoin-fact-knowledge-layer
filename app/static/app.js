/**
 * Fact Knowledge Layer Frontend Application Logic
 */

let currentTab = 'showcase';
let activeDataset = 'delhivery';
let allFacts = [];
let allRelationships = [];
let allDocuments = [];
let evaluationCases = [];
let selectedUploadFile = null;

// Initialization
document.addEventListener('DOMContentLoaded', () => {
  loadAllData();
});

async function loadAllData() {
  await Promise.all([
    fetchStats(),
    fetchCases(),
    fetchRelationships(),
    fetchFacts(),
    fetchDocuments()
  ]);
}

// -------------------------------------------------------------
// 1. Data Fetching
// -------------------------------------------------------------
async function fetchStats() {
  try {
    const res = await fetch('/api/status');
    const data = await res.json();
    document.getElementById('statDocs').textContent = data.total_documents;
    document.getElementById('statFacts').textContent = data.total_facts;
    document.getElementById('statCorrob').textContent = data.corroborated_relationships;
    document.getElementById('statApparent').textContent = data.apparent_contradictions;
    document.getElementById('statGenuine').textContent = data.genuine_contradictions;
    
    if (data.active_dataset) {
      activeDataset = data.active_dataset;
      document.getElementById('datasetSelect').value = data.active_dataset;
    }
  } catch (err) {
    console.error('Failed to fetch stats:', err);
  }
}

async function fetchCases() {
  try {
    const res = await fetch('/api/cases');
    evaluationCases = await res.json();
    renderCases(evaluationCases);
  } catch (err) {
    console.error('Failed to fetch cases:', err);
  }
}

async function fetchRelationships() {
  try {
    const res = await fetch('/api/relationships');
    allRelationships = await res.json();
    renderRelationships(allRelationships);
  } catch (err) {
    console.error('Failed to fetch relationships:', err);
  }
}

async function fetchFacts() {
  try {
    const res = await fetch('/api/facts');
    allFacts = await res.json();
    renderFacts(allFacts);
  } catch (err) {
    console.error('Failed to fetch facts:', err);
  }
}

async function fetchDocuments() {
  try {
    const res = await fetch('/api/documents');
    allDocuments = await res.json();
    renderDocuments(allDocuments);
  } catch (err) {
    console.error('Failed to fetch documents:', err);
  }
}

// -------------------------------------------------------------
// 2. Tab Navigation
// -------------------------------------------------------------
function setTab(tabName) {
  currentTab = tabName;
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));

  const activePane = document.getElementById(`tab-${tabName}`);
  if (activePane) activePane.classList.add('active');

  // Activate button
  const buttons = document.querySelectorAll('.tab-btn');
  if (tabName === 'showcase' && buttons[0]) buttons[0].classList.add('active');
  if (tabName === 'relationships' && buttons[1]) buttons[1].classList.add('active');
  if (tabName === 'explorer' && buttons[2]) buttons[2].classList.add('active');
  if (tabName === 'documents' && buttons[3]) buttons[3].classList.add('active');
}

// -------------------------------------------------------------
// 3. Render Showcase 4 Cases
// -------------------------------------------------------------
function renderCases(cases) {
  const container = document.getElementById('casesContainer');
  if (!container) return;

  if (!cases || cases.length === 0) {
    container.innerHTML = '<div class="loading-state">No evaluation cases loaded.</div>';
    return;
  }

  container.innerHTML = cases.map(c => {
    let badgeClass = 'badge-corroborated';
    let badgeText = 'Corroborated';
    if (c.case_type === 'GENUINE_CONTRADICTION') {
      badgeClass = 'badge-genuine';
      badgeText = 'Genuine Contradiction';
    } else if (c.case_type === 'APPARENT_CONTRADICTION') {
      badgeClass = 'badge-apparent';
      badgeText = 'Apparent Contradiction (Context-Reconciled)';
    } else if (c.case_type === 'EXTRACTION_REASONING_FAILURE') {
      badgeClass = 'badge-failure';
      badgeText = 'Extraction / Reasoning Failure Case';
    }

    const sideA = c.evidence_a ? `
      <div class="evidence-side-card">
        <div class="evidence-header">
          <span class="evidence-doc-pill" title="${c.evidence_a.document_name}">
            📄 ${c.evidence_a.document_name}
          </span>
          <span class="page-badge">Page ${c.evidence_a.page_number}</span>
        </div>
        ${c.fact_a ? `<div class="stated-fact-value">${c.fact_a.attribute}: <strong>${c.fact_a.value}</strong></div>` : ''}
        <div class="quote-box">"${escapeHtml(c.evidence_a.quote)}"</div>
        <div class="context-tags">
          ${c.fact_a?.context?.temporal_period ? `<span class="context-tag">⏰ ${c.fact_a.context.temporal_period}</span>` : ''}
          ${c.fact_a?.context?.scope ? `<span class="context-tag">🎯 Scope: ${c.fact_a.context.scope}</span>` : ''}
          ${c.fact_a?.context?.unit ? `<span class="context-tag">📏 Unit: ${c.fact_a.context.unit}</span>` : ''}
        </div>
      </div>
    ` : '';

    const sideB = c.evidence_b ? `
      <div class="evidence-side-card">
        <div class="evidence-header">
          <span class="evidence-doc-pill" title="${c.evidence_b.document_name}">
            📄 ${c.evidence_b.document_name}
          </span>
          <span class="page-badge">Page ${c.evidence_b.page_number}</span>
        </div>
        ${c.fact_b ? `<div class="stated-fact-value">${c.fact_b.attribute}: <strong>${c.fact_b.value}</strong></div>` : ''}
        <div class="quote-box">"${escapeHtml(c.evidence_b.quote)}"</div>
        <div class="context-tags">
          ${c.fact_b?.context?.temporal_period ? `<span class="context-tag">⏰ ${c.fact_b.context.temporal_period}</span>` : ''}
          ${c.fact_b?.context?.scope ? `<span class="context-tag">🎯 Scope: ${c.fact_b.context.scope}</span>` : ''}
          ${c.fact_b?.context?.unit ? `<span class="context-tag">📏 Unit: ${c.fact_b.context.unit}</span>` : ''}
        </div>
      </div>
    ` : '';

    return `
      <div class="case-card">
        <div class="case-card-header">
          <div>
            <div class="case-badge-group">
              <span class="case-number">Case ${c.case_number} of 4</span>
              <span class="${badgeClass}">${badgeText}</span>
            </div>
            <h3 class="case-title">${escapeHtml(c.title)}</h3>
          </div>
        </div>
        
        <p class="case-desc">${escapeHtml(c.description)}</p>

        <div class="side-by-side">
          ${sideA}
          ${sideB}
        </div>

        <div class="reasoning-box">
          <div class="reasoning-title">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
            System Automated Reasoning Chain
          </div>
          <div class="reasoning-content">${escapeHtml(c.system_reasoning)}</div>
        </div>

        ${c.handling_or_improvement ? `
          <div class="reasoning-box" style="border-color: rgba(139, 92, 246, 0.3); background-color: #17162e;">
            <div class="reasoning-title" style="color: #c084fc;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
              Handling & Technical Improvement
            </div>
            <div class="reasoning-content">${escapeHtml(c.handling_or_improvement)}</div>
          </div>
        ` : ''}

        <div class="takeaway-box">
          <span class="takeaway-bold">Engineering Takeaway:</span>
          <span>${escapeHtml(c.technical_takeaway)}</span>
        </div>
      </div>
    `;
  }).join('');
}

// -------------------------------------------------------------
// 4. Render Relationships
// -------------------------------------------------------------
function renderRelationships(relationships) {
  const container = document.getElementById('relationshipsContainer');
  if (!container) return;

  if (!relationships || relationships.length === 0) {
    container.innerHTML = '<div class="loading-state">No relationships found matching criteria.</div>';
    return;
  }

  container.innerHTML = relationships.map(r => {
    let badgeClass = 'badge-corroborated';
    let badgeText = 'Corroborated';
    if (r.relationship_type === 'GENUINE_CONTRADICTION') {
      badgeClass = 'badge-genuine';
      badgeText = 'Genuine Contradiction';
    } else if (r.relationship_type === 'APPARENT_CONTRADICTION') {
      badgeClass = 'badge-apparent';
      badgeText = 'Apparent Contradiction (Contextual)';
    }

    const docA = r.fact_a ? r.fact_a.evidence.document_name : 'Document A';
    const docB = r.fact_b ? r.fact_b.evidence.document_name : 'Document B';
    const valA = r.fact_a ? r.fact_a.value : '-';
    const valB = r.fact_b ? r.fact_b.value : '-';

    return `
      <div class="rel-card">
        <div class="rel-card-top">
          <div class="rel-summary">${escapeHtml(r.comparison_summary)}</div>
          <span class="${badgeClass}">${badgeText}</span>
        </div>

        <div class="rel-comparison-grid">
          <div>
            <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.2rem;">${docA} (P. ${r.fact_a?.evidence?.page_number || '?'})</div>
            <div style="font-size: 0.95rem; font-weight: 700; color: #60a5fa;">${valA}</div>
            <div style="font-size: 0.75rem; color: #cbd5e1; margin-top: 0.25rem;">"${escapeHtml(r.fact_a?.evidence?.quote || '')}"</div>
          </div>
          <div>
            <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.2rem;">${docB} (P. ${r.fact_b?.evidence?.page_number || '?'})</div>
            <div style="font-size: 0.95rem; font-weight: 700; color: #38bdf8;">${valB}</div>
            <div style="font-size: 0.75rem; color: #cbd5e1; margin-top: 0.25rem;">"${escapeHtml(r.fact_b?.evidence?.quote || '')}"</div>
          </div>
        </div>

        <div class="reasoning-box" style="margin-bottom: 0;">
          <div class="reasoning-title">Reconciliation Reasoning</div>
          <div class="reasoning-content">${escapeHtml(r.reasoning)}</div>
        </div>
      </div>
    `;
  }).join('');
}

function filterRelationships() {
  const typeFilter = document.getElementById('relFilterType').value;
  if (typeFilter === 'ALL') {
    renderRelationships(allRelationships);
  } else {
    const filtered = allRelationships.filter(r => r.relationship_type === typeFilter);
    renderRelationships(filtered);
  }
}

// -------------------------------------------------------------
// 5. Render Facts Explorer
// -------------------------------------------------------------
function renderFacts(facts) {
  const container = document.getElementById('factsContainer');
  if (!container) return;

  if (!facts || facts.length === 0) {
    container.innerHTML = '<div class="loading-state">No facts found.</div>';
    return;
  }

  container.innerHTML = facts.map(f => {
    return `
      <div class="fact-card">
        <div class="fact-card-top">
          <div class="fact-entity">${escapeHtml(f.entity)}</div>
          <div class="fact-attribute">${escapeHtml(f.attribute)}</div>
          <div class="fact-val-badge">${escapeHtml(f.value)}</div>
          <div class="context-tags">
            ${f.context?.temporal_period ? `<span class="context-tag">⏰ ${f.context.temporal_period}</span>` : ''}
            ${f.context?.scope ? `<span class="context-tag">🎯 ${f.context.scope}</span>` : ''}
            <span class="context-tag">🏷️ ${f.category}</span>
          </div>
        </div>
        <div class="fact-evidence-link" onclick="openEvidenceModal('${f.id}')">
          <span>📄 ${f.evidence.document_name}</span>
          <span class="page-badge">Page ${f.evidence.page_number}</span>
        </div>
      </div>
    `;
  }).join('');
}

function filterFacts() {
  const q = (document.getElementById('factSearchInput').value || '').toLowerCase();
  const cat = document.getElementById('factCategoryFilter').value;

  const filtered = allFacts.filter(f => {
    const matchCat = (cat === 'ALL') || (f.category.toLowerCase() === cat.toLowerCase());
    const matchQ = !q || (
      f.entity.toLowerCase().includes(q) ||
      f.attribute.toLowerCase().includes(q) ||
      f.value.toLowerCase().includes(q) ||
      f.evidence.quote.toLowerCase().includes(q)
    );
    return matchCat && matchQ;
  });

  renderFacts(filtered);
}

// -------------------------------------------------------------
// 6. Render Source Documents
// -------------------------------------------------------------
function renderDocuments(docs) {
  const container = document.getElementById('documentsContainer');
  if (!container) return;

  container.innerHTML = docs.map(d => {
    const sizeMb = (d.file_size_bytes / (1024 * 1024)).toFixed(2);
    return `
      <div class="doc-card">
        <div class="doc-card-title">📄 ${escapeHtml(d.title)}</div>
        <div class="doc-card-meta">
          <div><strong>Filename:</strong> ${d.filename}</div>
          <div><strong>Total Pages:</strong> ${d.total_pages} pages</div>
          <div><strong>Size:</strong> ${sizeMb} MB</div>
          <div><strong>Indexed Facts:</strong> ${d.facts_count} grounded facts</div>
          <div><strong>Ingestion Time:</strong> ${d.indexed_at}</div>
        </div>
        <button class="btn btn-secondary" style="width: 100%; font-size: 0.8rem;" onclick="filterFactsByDoc('${d.id}')">
          View Extracted Facts
        </button>
      </div>
    `;
  }).join('');
}

function filterFactsByDoc(docId) {
  setTab('explorer');
  const filtered = allFacts.filter(f => f.evidence.document_id === docId);
  renderFacts(filtered);
}

// -------------------------------------------------------------
// 7. Dataset Switching
// -------------------------------------------------------------
async function switchDataset(datasetName) {
  try {
    const res = await fetch('/api/dataset/load', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dataset: datasetName })
    });
    const result = await res.json();
    await loadAllData();
  } catch (err) {
    console.error('Failed to switch dataset:', err);
  }
}

// -------------------------------------------------------------
// 8. Modals (Evidence & Upload)
// -------------------------------------------------------------
function openEvidenceModal(factId) {
  const fact = allFacts.find(f => f.id === factId);
  if (!fact) return;

  const content = document.getElementById('evidenceModalContent');
  content.innerHTML = `
    <div style="margin-bottom: 1rem;">
      <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.25rem;">Entity & Metric</div>
      <div style="font-size: 1.1rem; font-weight: 700;">${escapeHtml(fact.entity)} — ${escapeHtml(fact.attribute)}</div>
      <div style="font-size: 1.25rem; font-weight: 800; color: #38bdf8; margin: 0.35rem 0;">${escapeHtml(fact.value)}</div>
    </div>

    <div style="margin-bottom: 1rem;">
      <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.25rem;">Source Grounding</div>
      <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.5rem;">
        <span class="evidence-doc-pill">📄 ${fact.evidence.document_name}</span>
        <span class="page-badge">Page ${fact.evidence.page_number}</span>
      </div>
      <div class="quote-box">"${escapeHtml(fact.evidence.quote)}"</div>
    </div>

    ${fact.evidence.surrounding_context ? `
      <div style="margin-bottom: 1rem;">
        <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.25rem;">Surrounding Excerpt / Section Context</div>
        <div style="font-size: 0.85rem; color: #cbd5e1; background: #0f172a; padding: 0.75rem; border-radius: 6px; font-family: var(--font-mono);">
          ${escapeHtml(fact.evidence.surrounding_context)}
        </div>
      </div>
    ` : ''}

    <div>
      <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.25rem;">Structured Context Qualifiers</div>
      <div class="context-tags">
        ${fact.context.temporal_period ? `<span class="context-tag">⏰ Period: ${fact.context.temporal_period}</span>` : ''}
        ${fact.context.scope ? `<span class="context-tag">🎯 Scope: ${fact.context.scope}</span>` : ''}
        ${fact.context.unit ? `<span class="context-tag">📏 Unit: ${fact.context.unit}</span>` : ''}
        ${fact.context.accounting_or_source_note ? `<span class="context-tag">📋 Note: ${fact.context.accounting_or_source_note}</span>` : ''}
      </div>
    </div>
  `;

  document.getElementById('evidenceModal').classList.add('open');
}

function closeEvidenceModal() {
  document.getElementById('evidenceModal').classList.remove('open');
}

function openUploadModal() {
  selectedUploadFile = null;
  document.getElementById('fileInput').value = '';
  document.getElementById('selectedFileInfo').style.display = 'none';
  document.getElementById('uploadStatus').style.display = 'none';
  document.getElementById('uploadSubmitBtn').disabled = true;
  document.getElementById('uploadModal').classList.add('open');
}

function closeUploadModal() {
  document.getElementById('uploadModal').classList.remove('open');
}

function handleFileSelected(file) {
  if (!file) return;
  if (!file.name.toLowerCase().endsWith('.pdf')) {
    alert('Please select a valid PDF file.');
    return;
  }

  selectedUploadFile = file;
  document.getElementById('selectedFileName').textContent = file.name;
  document.getElementById('selectedFileSize').textContent = (file.size / (1024 * 1024)).toFixed(2) + ' MB';
  document.getElementById('selectedFileInfo').style.display = 'flex';
  document.getElementById('uploadSubmitBtn').disabled = false;
}

// Drag & drop dropzone handlers
const dropzone = document.getElementById('dropzone');
if (dropzone) {
  dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.style.borderColor = '#3b82f6';
  });
  dropzone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropzone.style.borderColor = 'var(--color-border-light)';
  });
  dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.style.borderColor = 'var(--color-border-light)';
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  });
}

async function submitUpload() {
  if (!selectedUploadFile) return;

  const statusEl = document.getElementById('uploadStatus');
  const submitBtn = document.getElementById('uploadSubmitBtn');

  statusEl.className = 'upload-status loading';
  statusEl.textContent = 'Uploading, parsing layout, extracting facts, and incrementally reconciling...';
  statusEl.style.display = 'block';
  submitBtn.disabled = true;

  const formData = new FormData();
  formData.append('file', selectedUploadFile);

  try {
    const res = await fetch('/api/documents/upload', {
      method: 'POST',
      body: formData
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Upload failed');
    }

    const data = await res.json();
    statusEl.className = 'upload-status success';
    statusEl.textContent = `Success! Ingested ${data.document.filename} (${data.facts_extracted} facts extracted, ${data.new_relationships_formed} new cross-document relationships formed).`;

    // Refresh UI data
    await loadAllData();
    setTimeout(() => {
      closeUploadModal();
      setTab('relationships');
    }, 1800);
  } catch (err) {
    statusEl.className = 'upload-status error';
    statusEl.textContent = `Error: ${err.message}`;
    submitBtn.disabled = false;
  }
}

// Helper utility
function escapeHtml(text) {
  if (!text) return '';
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
