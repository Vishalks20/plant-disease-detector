/* Plant Disease Detector — Frontend */

const fileInput     = document.getElementById("fileInput");
const dropzone      = document.getElementById("dropzone");
const previewSection = document.getElementById("previewSection");
const previewImg    = document.getElementById("previewImg");
const analyzeBtn    = document.getElementById("analyzeBtn");
const clearBtn      = document.getElementById("clearBtn");
const resultCard    = document.getElementById("resultCard");
const resultHeader  = document.getElementById("resultHeader");
const resultBody    = document.getElementById("resultBody");

let selectedFile = null;

// ── File selection ──────────────────────────────────────────────────────────
fileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (file) handleFile(file);
});

// ── Drag & Drop ─────────────────────────────────────────────────────────────
dropzone.addEventListener("dragover", (e) => { e.preventDefault(); dropzone.classList.add("drag-over"); });
dropzone.addEventListener("dragleave", () => dropzone.classList.remove("drag-over"));
dropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropzone.classList.remove("drag-over");
  const file = e.dataTransfer.files[0];
  if (file) handleFile(file);
});
dropzone.addEventListener("click", () => fileInput.click());

function handleFile(file) {
  if (!file.type.startsWith("image/")) {
    alert("Please upload an image file (JPG, PNG, WEBP).");
    return;
  }
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImg.src = e.target.result;
    dropzone.style.display = "none";
    previewSection.style.display = "flex";
    resultCard.style.display = "none";
  };
  reader.readAsDataURL(file);
}

// ── Clear ───────────────────────────────────────────────────────────────────
clearBtn.addEventListener("click", () => {
  selectedFile = null;
  fileInput.value = "";
  previewImg.src = "";
  previewSection.style.display = "none";
  dropzone.style.display = "flex";
  resultCard.style.display = "none";
});

// ── Analyze ─────────────────────────────────────────────────────────────────
analyzeBtn.addEventListener("click", async () => {
  if (!selectedFile) return;

  analyzeBtn.disabled = true;
  analyzeBtn.innerHTML = '<span class="spinner"></span>Analyzing...';

  const formData = new FormData();
  formData.append("image", selectedFile);
  formData.append("top_k", "5");

  try {
    const resp = await fetch("/api/predict", { method: "POST", body: formData });
    const data = await resp.json();
    renderResult(data);
  } catch (err) {
    renderError("Network error. Please try again.");
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = "🔬 Analyze";
  }
});

// ── Render Result ───────────────────────────────────────────────────────────
function renderResult(data) {
  resultCard.style.display = "block";

  if (!data.success) {
    renderError(data.error || "Prediction failed.");
    return;
  }

  const isHealthy = data.is_healthy;
  const headerClass = isHealthy ? "" : "disease";
  const icon = isHealthy ? "✅" : "⚠️";
  const info = data.disease_info || {};

  resultHeader.className = `result-header ${headerClass}`;
  resultHeader.innerHTML = `
    <div class="plant-tag">🌱 ${data.plant}</div>
    <h2>${icon} ${data.disease}</h2>
    <span class="confidence-badge">Confidence: ${data.confidence_pct}</span>
  `;

  let bodyHTML = "";

  if (!isHealthy) {
    bodyHTML += `
      <div class="info-grid">
        <div class="info-block">
          <h4>Cause</h4>
          <p>${info.cause || "N/A"}</p>
        </div>
        <div class="info-block">
          <h4>Symptoms</h4>
          <p>${info.symptoms || "N/A"}</p>
        </div>
      </div>
    `;

    if (info.treatment && info.treatment.length) {
      bodyHTML += `<p class="section-title">💊 Treatment</p><ul class="treatment-list">`;
      info.treatment.forEach(t => { bodyHTML += `<li>${t}</li>`; });
      bodyHTML += `</ul>`;
    }

    if (info.prevention && info.prevention.length) {
      bodyHTML += `<p class="section-title">🛡️ Prevention</p><ul class="prevention-list">`;
      info.prevention.forEach(p => { bodyHTML += `<li>${p}</li>`; });
      bodyHTML += `</ul>`;
    }
  } else {
    bodyHTML += `<p style="color:#047857;font-size:1.05rem;margin-bottom:1.5rem;">
      Your plant looks healthy! Continue regular monitoring and care.
    </p>`;
    if (info.prevention && info.prevention.length) {
      bodyHTML += `<p class="section-title">🛡️ Maintenance Tips</p><ul class="prevention-list">`;
      info.prevention.forEach(p => { bodyHTML += `<li>${p}</li>`; });
      bodyHTML += `</ul>`;
    }
  }

  // Confidence bars
  if (data.top_predictions && data.top_predictions.length) {
    bodyHTML += `<div class="confidence-bars"><p class="section-title">📊 Top Predictions</p>`;
    data.top_predictions.forEach(pred => {
      const pct = (pred.confidence * 100).toFixed(1);
      const label = pred.class.replace(/___/g, " — ").replace(/_/g, " ");
      bodyHTML += `
        <div class="bar-item">
          <div class="bar-label"><span>${label}</span><span>${pct}%</span></div>
          <div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div>
        </div>
      `;
    });
    bodyHTML += `</div>`;
  }

  resultBody.innerHTML = bodyHTML;
  resultCard.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderError(message) {
  resultCard.style.display = "block";
  resultHeader.className = "result-header disease";
  resultHeader.innerHTML = `<h2>❌ Error</h2>`;
  resultBody.innerHTML = `<p style="color:#b45309;padding:1rem 0;">${message}</p>`;
}
