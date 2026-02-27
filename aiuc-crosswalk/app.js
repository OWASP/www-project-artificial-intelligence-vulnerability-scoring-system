/* Enhanced AIUC-AIVSS Crosswalk Dashboard */
(function(){
  const data = window.CROSSWALK_DATA;
  const $ = (id) => document.getElementById(id);
  const $$ = (sel) => document.querySelectorAll(sel);

  // Color palette for charts
  const COLORS = [
    '#5aa7ff', '#a78bfa', '#34d399', '#fbbf24', '#f87171',
    '#60a5fa', '#c084fc', '#4ade80', '#facc15', '#fb923c'
  ];

  const RISK_COLORS = {
    'Agent Untraceability': '#5aa7ff',
    'Agent Goal & Instruction Manipulation': '#a78bfa',
    'Agent Access Control Violation': '#34d399',
    'Agent Supply Chain & Dependency Risk': '#fbbf24',
    'Agentic AI Tool Misuse': '#f87171',
    'Agent Cascading Failures': '#60a5fa',
    'Agent Memory & Context Manipulation': '#c084fc',
    'Insecure Agent Critical Systems Interaction': '#4ade80',
    'Agent Orchestration & Multi-Agent Exploitation': '#facc15',
    'Agent Identity Impersonation': '#fb923c'
  };

  function uniq(arr) { return Array.from(new Set(arr)).sort(); }

  function escapeHtml(str) {
    return String(str ?? "").replace(/[&<>"']/g, s => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
    }[s]));
  }

  // AIUC mapping count: for each risk, count AIUC-confirmed primary.
  // For risks with 0 primary, count AIUC-confirmed secondary instead.
  function getAIUCRiskCounts() {
    const mapped = data.requirements.filter(r => r.AIUC_Mapped);
    const counts = {};
    const risks = data.aivss_core_risks || [];
    risks.forEach(risk => {
      const primary = mapped.filter(r => r.AIVSS_Primary === risk).length;
      counts[risk] = primary > 0
        ? primary
        : mapped.filter(r => r.AIVSS_Secondary === risk).length;
    });
    return counts;
  }

  // Tab Navigation
  function initTabs() {
    $$('.tab').forEach(tab => {
      tab.addEventListener('click', () => {
        $$('.tab').forEach(t => t.classList.remove('active'));
        $$('.tab-content').forEach(c => c.classList.remove('active'));
        tab.classList.add('active');
        $(`tab-${tab.dataset.tab}`).classList.add('active');
      });
    });
  }

  // Meta Information
  function renderMeta() {
    const m = data.meta || {};
    
    $("meta").innerHTML = `
      <div>
        <span class="chip">Generated</span> ${escapeHtml(m.generated_at || "")} 
        <span class="chip">${escapeHtml(m.mapping_version || "")}</span>
      </div>
    `;
  }

  // Summary Cards
  function renderCards() {
    const totalReq = data.requirements.length;
    const riskCounts = getAIUCRiskCounts();
    const mappedCount = Object.values(riskCounts).reduce((a, b) => a + b, 0);
    const unmappedCount = totalReq - mappedCount;
    const totalCtrl = data.controls.length;
    const coveredRisks = Object.values(riskCounts).filter(c => c > 0).length;

    $("summaryCards").innerHTML = `
      <div class="card">
        <h3>Total Requirements</h3>
        <div class="big">${totalReq}</div>
        <div class="small">Across 6 principles</div>
      </div>
      <div class="card">
        <h3>Mapped to AIVSS</h3>
        <div class="big" style="color:var(--success)">${mappedCount}</div>
        <div class="small">${unmappedCount} unmapped</div>
      </div>
      <div class="card">
        <h3>Controls/Evidence</h3>
        <div class="big">${totalCtrl}</div>
        <div class="small">Supporting requirements</div>
      </div>
      <div class="card">
        <h3>AIVSS Risks Covered</h3>
        <div class="big" style="color:var(--accent)">${coveredRisks} / 10</div>
        <div class="small">${10 - coveredRisks} gap(s)</div>
      </div>
    `;
  }

  // Bar Charts
  function renderBarCharts() {
    const reqByRisk = getAIUCRiskCounts();
    const ctrlByRisk = {};
    
    data.controls.forEach(c => {
      if (c.AIVSS_Primary) ctrlByRisk[c.AIVSS_Primary] = (ctrlByRisk[c.AIVSS_Primary] || 0) + 1;
    });

    const maxReq = Math.max(...Object.values(reqByRisk), 1);
    const maxCtrl = Math.max(...Object.values(ctrlByRisk), 1);

    const renderBars = (container, counts, max) => {
      const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);
      container.innerHTML = sorted.map(([risk, count]) => `
        <div class="bar-row">
          <div class="bar-label" title="${escapeHtml(risk)}">${escapeHtml(risk)}</div>
          <div class="bar-container">
            <div class="bar-fill" style="width:${(count / max) * 100}%; background:${RISK_COLORS[risk] || '#5aa7ff'}">
              <span class="bar-value">${count}</span>
            </div>
          </div>
        </div>
      `).join('');
    };

    renderBars($('reqChart'), reqByRisk, maxReq);
    renderBars($('ctrlChart'), ctrlByRisk, maxCtrl);
  }

  // Confidence Chart
  function renderConfidenceChart() {
    const all = [...data.requirements, ...data.controls];
    const high = all.filter(r => r.Confidence === 'High').length;
    const medium = all.filter(r => r.Confidence === 'Medium').length;
    const low = all.filter(r => r.Confidence === 'Low').length;
    const total = all.length || 1;

    $('confidenceChart').innerHTML = `
      <div class="conf-item">
        <div class="conf-circle" style="--percent:${(high/total)*100}%; --fill-color:var(--success)">
          <span>${high}</span>
        </div>
        <div class="conf-label">High (${((high/total)*100).toFixed(0)}%)</div>
      </div>
      <div class="conf-item">
        <div class="conf-circle" style="--percent:${(medium/total)*100}%; --fill-color:var(--warning)">
          <span>${medium}</span>
        </div>
        <div class="conf-label">Medium (${((medium/total)*100).toFixed(0)}%)</div>
      </div>
      <div class="conf-item">
        <div class="conf-circle" style="--percent:${(low/total)*100}%; --fill-color:var(--danger)">
          <span>${low}</span>
        </div>
        <div class="conf-label">Low (${((low/total)*100).toFixed(0)}%)</div>
      </div>
    `;
  }

  // Review Status Chart
  function renderReviewStatus() {
    const all = [...data.requirements, ...data.controls];
    const ok = all.filter(r => r.Review_Priority === 'OK').length;
    const p1 = all.filter(r => r.Review_Priority === 'P1').length;
    const p2 = all.filter(r => r.Review_Priority === 'P2').length;
    const p0 = all.filter(r => r.Review_Priority === 'P0').length;

    $('reviewStatusChart').innerHTML = `
      <div class="status-card status-ok" onclick="filterByReview('OK')">
        <div class="count">${ok}</div>
        <div class="label">OK - Ready</div>
      </div>
      <div class="status-card status-p1" onclick="filterByReview('P1')">
        <div class="count">${p1}</div>
        <div class="label">P1 - Review Suggested</div>
      </div>
      <div class="status-card status-p2" onclick="filterByReview('P2')">
        <div class="count">${p2}</div>
        <div class="label">P2 - Minor Issues</div>
      </div>
      ${p0 > 0 ? `
        <div class="status-card" style="background:rgba(248,81,73,0.2);border:1px solid var(--danger)" onclick="filterByReview('P0')">
          <div class="count">${p0}</div>
          <div class="label">P0 - Critical</div>
        </div>
      ` : ''}
    `;
  }

  // Make filterByReview global
  window.filterByReview = function(status) {
    $$('.tab').forEach(t => t.classList.remove('active'));
    $$('.tab-content').forEach(c => c.classList.remove('active'));
    document.querySelector('[data-tab="browse"]').classList.add('active');
    $('tab-browse').classList.add('active');
    $('reviewFilter').value = status;
    renderTable();
  };

  // Sankey Diagram
  function renderSankey() {
    const mapped = data.requirements.filter(r => r.AIUC_Mapped);
    const principles = uniq(data.requirements.map(r => r.Principle).filter(Boolean));
    const risks = data.aivss_core_risks || [];
    
    // Determine which risks have primary AIUC mappings
    const primaryPerRisk = {};
    mapped.forEach(r => {
      primaryPerRisk[r.AIVSS_Primary] = (primaryPerRisk[r.AIVSS_Primary] || 0) + 1;
    });

    // Count flows: primary always; secondary only for risks with 0 primary
    const flows = {};
    const riskTotals = getAIUCRiskCounts();
    mapped.forEach(r => {
      const pKey = `${r.Principle}|${r.AIVSS_Primary}`;
      flows[pKey] = (flows[pKey] || 0) + 1;
      if (r.AIVSS_Secondary && !primaryPerRisk[r.AIVSS_Secondary]) {
        const sKey = `${r.Principle}|${r.AIVSS_Secondary}`;
        flows[sKey] = (flows[sKey] || 0) + 1;
      }
    });

    const nodeHeight = 30;
    const padding = 10;
    const leftX = 50;
    const rightX = 700;
    const svgHeight = Math.max(principles.length, risks.length) * (nodeHeight + padding) + 100;

    // Left nodes: count AIUC-mapped per principle
    const leftNodes = principles.map((p, i) => ({
      name: p,
      y: 50 + i * (nodeHeight + padding),
      total: mapped.filter(r => r.Principle === p).length
    }));

    const rightNodes = risks.map((r, i) => ({
      name: r,
      y: 50 + i * (nodeHeight + padding * 0.8),
      total: riskTotals[r] || 0
    }));

    // Generate paths
    const paths = Object.entries(flows).map(([key, count]) => {
      const [principle, risk] = key.split('|');
      const left = leftNodes.find(n => n.name === principle);
      const right = rightNodes.find(n => n.name === risk);
      if (!left || !right) return '';
      
      const x1 = leftX + 150;
      const y1 = left.y + nodeHeight / 2;
      const x2 = rightX;
      const y2 = right.y + nodeHeight / 2;
      const cx = (x1 + x2) / 2;
      
      return `
        <path class="sankey-link" 
              d="M${x1},${y1} C${cx},${y1} ${cx},${y2} ${x2},${y2}"
              stroke="${RISK_COLORS[risk] || '#5aa7ff'}"
              stroke-width="${Math.max(count * 2, 2)}"
              data-principle="${escapeHtml(principle)}"
              data-risk="${escapeHtml(risk)}"
              data-count="${count}">
          <title>${escapeHtml(principle)} → ${escapeHtml(risk)}: ${count}</title>
        </path>
      `;
    }).join('');

    // Generate nodes
    const leftRects = leftNodes.map(n => `
      <g class="sankey-node" transform="translate(${leftX},${n.y})">
        <rect width="150" height="${nodeHeight}" rx="4" fill="var(--panel-light)" stroke="var(--border)"/>
        <text x="75" y="${nodeHeight/2 + 4}" text-anchor="middle" fill="var(--text)" font-size="11">${escapeHtml(n.name)}</text>
        <text x="145" y="${nodeHeight/2 + 4}" text-anchor="end" fill="var(--muted)" font-size="10">${n.total}</text>
      </g>
    `).join('');

    const rightRects = rightNodes.filter(n => n.total > 0).map(n => `
      <g class="sankey-node" transform="translate(${rightX},${n.y})">
        <rect width="200" height="${nodeHeight}" rx="4" fill="${RISK_COLORS[n.name] || 'var(--panel-light)'}" fill-opacity="0.3" stroke="${RISK_COLORS[n.name] || 'var(--border)'}"/>
        <text x="10" y="${nodeHeight/2 + 4}" fill="var(--text)" font-size="10">${escapeHtml(n.name.substring(0, 30))}</text>
        <text x="190" y="${nodeHeight/2 + 4}" text-anchor="end" fill="var(--text)" font-size="11" font-weight="bold">${n.total}</text>
      </g>
    `).join('');

    $('sankeyDiagram').innerHTML = `
      <svg class="sankey-svg" viewBox="0 0 950 ${svgHeight}" preserveAspectRatio="xMidYMid meet">
        ${paths}
        ${leftRects}
        ${rightRects}
        <text x="${leftX + 75}" y="30" text-anchor="middle" fill="var(--muted)" font-size="12" font-weight="600">AIUC Principles</text>
        <text x="${rightX + 100}" y="30" text-anchor="middle" fill="var(--muted)" font-size="12" font-weight="600">AIVSS Core Risks</text>
      </svg>
    `;
  }

  // ASI Bridge
  function renderASIBridge() {
    const bridge = data.asi_bridge || [];
    $('asiBridge').innerHTML = bridge.map(b => `
      <div class="asi-card">
        <div class="asi-id">${escapeHtml(b.ASI_ID)}</div>
        <div class="asi-title">${escapeHtml(b.ASI_Title)}</div>
        <div class="asi-arrow">↓ maps to</div>
        <div class="asi-target" style="border-left:3px solid ${RISK_COLORS[b.AIVSS_Primary] || 'var(--accent)'}">
          ${escapeHtml(b.AIVSS_Primary || 'Not mapped')}
        </div>
      </div>
    `).join('');
  }

  // Heatmap Matrix
  function renderHeatmap() {
    const principles = uniq(data.requirements.map(r => r.Principle).filter(Boolean));
    const risks = data.aivss_core_risks || [];
    const mapped = data.requirements.filter(r => r.AIUC_Mapped);
    
    // Determine which risks lack primary AIUC mappings
    const primaryPerRisk = {};
    mapped.forEach(r => {
      primaryPerRisk[r.AIVSS_Primary] = (primaryPerRisk[r.AIVSS_Primary] || 0) + 1;
    });
    
    // Build matrix using AIUC counting logic
    const matrix = {};
    principles.forEach(p => {
      matrix[p] = {};
      risks.forEach(r => matrix[p][r] = 0);
    });
    
    mapped.forEach(r => {
      if (r.Principle && r.AIVSS_Primary) {
        matrix[r.Principle][r.AIVSS_Primary]++;
      }
      if (r.Principle && r.AIVSS_Secondary && !primaryPerRisk[r.AIVSS_Secondary]) {
        matrix[r.Principle][r.AIVSS_Secondary]++;
      }
    });

    const maxVal = Math.max(...Object.values(matrix).flatMap(r => Object.values(r)), 1);

    const headerCells = risks.map(r => 
      `<th title="${escapeHtml(r)}">${escapeHtml(r.split(' ').slice(0, 2).join(' '))}</th>`
    ).join('');

    const rows = principles.map(p => {
      const cells = risks.map(r => {
        const val = matrix[p][r] || 0;
        const intensity = val / maxVal;
        const bg = val > 0 
          ? `rgba(90, 167, 255, ${0.2 + intensity * 0.6})` 
          : 'transparent';
        return `
          <td onclick="filterByCell('${escapeHtml(p)}', '${escapeHtml(r)}')" 
              title="${escapeHtml(p)} × ${escapeHtml(r)}: ${val}">
            <div class="heatmap-cell" style="background:${bg}">${val || '-'}</div>
          </td>
        `;
      }).join('');
      return `<tr><th>${escapeHtml(p)}</th>${cells}</tr>`;
    }).join('');

    $('heatmapMatrix').innerHTML = `
      <table class="heatmap-table">
        <thead><tr><th></th>${headerCells}</tr></thead>
        <tbody>${rows}</tbody>
      </table>
    `;
  }

  window.filterByCell = function(principle, risk) {
    $$('.tab').forEach(t => t.classList.remove('active'));
    $$('.tab-content').forEach(c => c.classList.remove('active'));
    document.querySelector('[data-tab="browse"]').classList.add('active');
    $('tab-browse').classList.add('active');
    $('principleFilter').value = principle;
    $('aivssFilter').value = risk;
    renderTable();
  };


  // Data Table (Browse tab)
  function buildFilters() {
    const aivss = ["", ...(data.aivss_core_risks || [])];
    $("aivssFilter").innerHTML = aivss.map(v => 
      `<option value="${escapeHtml(v)}">${v ? escapeHtml(v) : "All"}</option>`
    ).join("");

    const asi = ["", ...(data.asi_bridge || []).map(r => r.ASI_ID)];
    $("asiFilter").innerHTML = asi.map(v => 
      `<option value="${escapeHtml(v)}">${v ? escapeHtml(v) : "All"}</option>`
    ).join("");

    const principles = uniq([
      ...data.requirements.map(r => r.Principle).filter(Boolean),
      ...data.controls.map(r => r.Principle).filter(Boolean),
    ]);
    $("principleFilter").innerHTML = ["", ...principles].map(v => 
      `<option value="${escapeHtml(v)}">${v ? escapeHtml(v) : "All"}</option>`
    ).join("");
  }

  function currentRows() {
    return data.requirements;
  }

  function columnsFor() {
    return [
      { k: "RequirementID", label: "ID" },
      { k: "Principle", label: "Principle" },
      { k: "RequirementTitle", label: "Title" },
      { k: "AIVSS_Primary", label: "AIVSS Primary" },
      { k: "AIVSS_Secondary", label: "Secondary" },
      { k: "Confidence", label: "Conf" },
      { k: "Review_Priority", label: "Review" },
    ];
  }

  function matches(row) {
    const aivss = $("aivssFilter").value;
    const asi = $("asiFilter").value;
    const principle = $("principleFilter").value;
    const conf = $("confidenceFilter").value;
    const review = $("reviewFilter").value;
    const changedOnly = $("changedOnly").checked;
    const q = ($("searchBox").value || "").trim().toLowerCase();

    if (aivss && row.AIVSS_Primary !== aivss) return false;
    if (asi && (row.ASI_ID || "") !== asi) return false;
    if (principle && (row.Principle || "") !== principle) return false;
    if (conf && (row.Confidence || "") !== conf) return false;
    if (review && (row.Review_Priority || "") !== review) return false;
    if (changedOnly && (row.Review_Change_Flag || "") !== "Y") return false;

    if (q) {
      const blob = JSON.stringify(row).toLowerCase();
      if (!blob.includes(q)) return false;
    }
    return true;
  }

  function renderTable() {
    const rows = currentRows().filter(matches);
    $("resultsCount").textContent = `${rows.length} result(s)`;

    const cols = columnsFor();
    $("resultsTable").querySelector("thead").innerHTML = 
      `<tr>${cols.map(c => `<th>${escapeHtml(c.label)}</th>`).join("")}</tr>`;

    const tbody = rows.map((r, idx) => {
      const tds = cols.map(c => {
        let val = r[c.k];
        if (c.k === "Confidence" && val) {
          return `<td><span class="chip ${String(val).toLowerCase()}">${escapeHtml(val)}</span></td>`;
        }
        if (c.k === "Review_Priority" && val) {
          return `<td><span class="chip">${escapeHtml(val)}</span></td>`;
        }
        if (c.k === "AIVSS_Primary" && val) {
          return `<td><span class="chip" style="border-color:${RISK_COLORS[val] || 'var(--border)'}">${escapeHtml(val?.substring(0, 25))}${val?.length > 25 ? '...' : ''}</span></td>`;
        }
        if (c.k === "RequirementTitle" && val) {
          return `<td title="${escapeHtml(val)}">${escapeHtml(val?.substring(0, 50))}${val?.length > 50 ? '...' : ''}</td>`;
        }
        return `<td>${escapeHtml(val ?? "")}</td>`;
      }).join("");
      return `<tr data-idx="${idx}">${tds}</tr>`;
    }).join("");

    $("resultsTable").querySelector("tbody").innerHTML = tbody;

    $("resultsTable").querySelectorAll("tbody tr").forEach(tr => {
      tr.addEventListener("click", () => {
        const idx = Number(tr.getAttribute("data-idx"));
        openDetails(rows[idx]);
      });
    });

    $("exportBtn").onclick = () => exportCsv(rows, cols.map(c => c.k));
  }

  function kv(label, value) {
    return `<div class="kv"><div class="k">${escapeHtml(label)}</div><div class="v">${value}</div></div>`;
  }

  function openDetails(row) {
    const aars = (() => {
      try { return JSON.parse(row.AARS_Factors_Suggested || "{}"); }
      catch (e) { return {}; }
    })();
    const aarsPretty = Object.keys(aars).length 
      ? `<pre>${escapeHtml(JSON.stringify(aars, null, 2))}</pre>` 
      : "<span class='chip'>None</span>";

    const header = `<span class="chip">Requirement</span> <span class="chip">${escapeHtml(row.RequirementID)}</span> ${escapeHtml(row.RequirementTitle || "")}`;

    const bodyParts = [];
    bodyParts.push(`<div style="margin-bottom:16px;font-size:14px;">${header}</div>`);
    bodyParts.push(kv("Principle", escapeHtml(row.Principle || "")));
    bodyParts.push(kv("AIVSS Primary", `<span class="chip" style="border-color:${RISK_COLORS[row.AIVSS_Primary]}">${escapeHtml(row.AIVSS_Primary || "")}</span>`));
    bodyParts.push(kv("AIVSS Secondary", escapeHtml(row.AIVSS_Secondary || "-")));
    bodyParts.push(kv("ASI Bridge", row.ASI_ID ? `<span class="chip">${escapeHtml(row.ASI_ID)}</span> ${escapeHtml(row.ASI_Title || "")}` : "<span class='chip'>None</span>"));
    bodyParts.push(kv("Confidence", `<span class="chip ${String(row.Confidence || "").toLowerCase()}">${escapeHtml(row.Confidence || "")}</span>`));
    bodyParts.push(kv("Review Priority", `<span class="chip">${escapeHtml(row.Review_Priority || "")}</span>`));
    bodyParts.push(kv("Full Requirement", `<pre>${escapeHtml(row.FullRequirement || "")}</pre>`));
    bodyParts.push(kv("Application", escapeHtml(row.Application || "")));
    bodyParts.push(kv("Frequency", escapeHtml(row.Frequency || "")));
    bodyParts.push(kv("Capabilities", escapeHtml(row.Capabilities || "")));
    bodyParts.push(kv("Rationale", `<pre>${escapeHtml(row.Rationale || "")}</pre>`));
    bodyParts.push(kv("AARS Factors", aarsPretty));

    if (row.Review_Checks_Failed) {
      bodyParts.push(kv("Checks Failed", `<pre>${escapeHtml(row.Review_Checks_Failed)}</pre>`));
    }

    $("detailsBody").innerHTML = bodyParts.join("");
    $("detailsPane").classList.add("open");
    $("closeDetails").onclick = () => $("detailsPane").classList.remove("open");
  }

  function exportCsv(rows, keys) {
    const header = keys.join(",");
    const lines = rows.map(r => {
      return keys.map(k => {
        let v = r[k];
        if (v === null || v === undefined) v = "";
        v = String(v).replace(/"/g, '""');
        if (v.search(/("|,|\n)/g) >= 0) v = `"${v}"`;
        return v;
      }).join(",");
    });
    const csv = [header, ...lines].join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "aiuc_aivss_requirements_filtered.csv";
    a.click();
    URL.revokeObjectURL(url);
  }

  function wire() {
    ["viewSelect", "aivssFilter", "asiFilter", "principleFilter", "confidenceFilter", "reviewFilter", "searchBox", "changedOnly"].forEach(id => {
      const el = $(id);
      if (el) {
        el.addEventListener("input", renderTable);
        el.addEventListener("change", renderTable);
      }
    });

    $("resetBtn").onclick = () => {
      $("aivssFilter").value = "";
      $("asiFilter").value = "";
      $("principleFilter").value = "";
      $("confidenceFilter").value = "";
      $("reviewFilter").value = "";
      $("searchBox").value = "";
      $("changedOnly").checked = false;
      renderTable();
    };
  }

  // Initialize everything
  function init() {
    initTabs();
    renderMeta();
    renderCards();
    renderBarCharts();
    renderConfidenceChart();
    renderReviewStatus();
    renderSankey();
    renderASIBridge();
    renderHeatmap();
    buildFilters();
    wire();
    renderTable();
  }

  init();
})();
