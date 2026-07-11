const DOMAIN_COLORS = {
  "Machine Learning": "#2563eb",
  Statistics: "#16a34a",
  "Business Analytics": "#f97316",
  "Data Science": "#8b5cf6",
  Leadership: "#dc2626",
  Communication: "#0ea5e9",
  "Digital Transformation": "#7c3aed",
  Business: "#f59e0b",
  "Project Management": "#14b8a6",
  "Soft Skills": "#ef4444",
  Other: "#64748b",
};

const RELATION_LABELS = {
  prerequisite: "Prerequisite",
  related: "Related concept",
  broader: "Broader topic",
  used_in: "Used in",
  application: "Application",
};

const state = {
  graph: null,
  cy: null,
  selectedNodeId: "",
  layout: "cose",
  searchQuery: "",
  searchResultIds: [],
  filters: {
    minImportance: 1,
    domains: new Set(),
    relationTypes: new Set(),
    courses: new Set(),
  },
};

const els = {
  graph: document.getElementById("graph"),
  tooltip: document.getElementById("tooltip"),
  searchInput: document.getElementById("graph-search"),
  searchResults: document.getElementById("search-results"),
  layoutSelect: document.getElementById("layout-select"),
  fitBtn: document.getElementById("fit-btn"),
  resetBtn: document.getElementById("reset-btn"),
  importanceRange: document.getElementById("importance-range"),
  importanceValue: document.getElementById("importance-value"),
  legend: document.getElementById("legend"),
  domainFilters: document.getElementById("domain-filters"),
  relationFilters: document.getElementById("relation-filters"),
  courseFilters: document.getElementById("course-filters"),
  stats: document.getElementById("stats"),
  detailEmpty: document.getElementById("detail-empty"),
  detailContent: document.getElementById("detail-content"),
  detailName: document.getElementById("detail-name"),
  detailMeta: document.getElementById("detail-meta"),
  detailDefinition: document.getElementById("detail-definition"),
  detailCore: document.getElementById("detail-core"),
  detailApplications: document.getElementById("detail-applications"),
  detailInterview: document.getElementById("detail-interview"),
  detailRelated: document.getElementById("detail-related"),
  detailCourses: document.getElementById("detail-courses"),
  detailOpen: document.getElementById("detail-open"),
  selectionSummary: document.getElementById("selection-summary"),
};

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function normalizeText(value) {
  return String(value ?? "")
    .trim()
    .toLowerCase();
}

function siteUrlFromMetadataPath(metadataPath, suffix = "metadata.json") {
  const normalized = String(metadataPath ?? "").replaceAll("\\", "/");
  const marker = "/knowledge_base/";
  const idx = normalized.lastIndexOf(marker);
  if (idx >= 0) {
    const rel = normalized.slice(idx + 1).replace(/metadata\.json$/i, suffix);
    return `../${encodeURI(rel)}`;
  }
  return `../${encodeURI(normalized.replace(/metadata\.json$/i, suffix))}`;
}

function conceptViewerUrl(metadataPath) {
  const normalized = String(metadataPath ?? "").replaceAll("\\", "/");
  const marker = "/knowledge_base/";
  const idx = normalized.lastIndexOf(marker);
  if (idx >= 0) {
    const rel = normalized.slice(idx + 1).replace(/metadata\.json$/i, "concept.md");
    return `./concept.html?path=${encodeURIComponent(`../${rel}`)}`;
  }
  return `./concept.html?path=${encodeURIComponent(normalized.replace(/metadata\.json$/i, "concept.md"))}`;
}

function domainColor(domain) {
  return DOMAIN_COLORS[domain] || DOMAIN_COLORS.Other;
}

function nodeSearchBlob(node) {
  return [
    node.concept_name,
    node.concept_key,
    node.domain,
    node.topic,
    ...(node.aliases || []),
    ...(node.prerequisites || []),
    ...(node.related_concepts || []),
    ...(node.broader_topics || []),
    ...(node.applications || []),
    ...(node.contributing_courses || []),
  ]
    .map(normalizeText)
    .join(" ");
}

function buildFallbackGraph(nodesPayload, edgesPayload) {
  const nodes = (nodesPayload.nodes || []).map((node) => {
    const metadataUrl = siteUrlFromMetadataPath(node.metadata_path, "metadata.json");
    return {
      ...node,
      aliases: [],
      prerequisites: [],
      related_concepts: [],
      broader_topics: [],
      applications: [],
      definition: "",
      core_idea: "",
      interview_notes: "",
      connected_edge_count: 0,
      degree: 0,
      metadata_url: metadataUrl,
      concept_url: conceptViewerUrl(node.metadata_path),
      search_terms: [
        node.concept_name,
        node.concept_key,
        node.domain,
        node.topic,
        ...(node.contributing_courses || []),
      ],
    };
  });
  const edges = edgesPayload.edges || [];
  const degree = new Map();
  edges.forEach((edge) => {
    degree.set(edge.source, (degree.get(edge.source) || 0) + 1);
    degree.set(edge.target, (degree.get(edge.target) || 0) + 1);
  });
  nodes.forEach((node) => {
    const count = degree.get(node.node_id) || 0;
    node.connected_edge_count = count;
    node.degree = count;
  });
  const domains = [...new Set(nodes.map((node) => node.domain).filter(Boolean))].sort();
  const multiCourse = nodes.filter((node) => (node.contributing_courses || []).length > 1).length;
  const relationCounts = edges.reduce((acc, edge) => {
    acc[edge.relation_type] = (acc[edge.relation_type] || 0) + 1;
    return acc;
  }, {});
  return {
    schema_version: 1,
    generated_at: nodesPayload.generated_at || edgesPayload.generated_at || "",
    stats: {
      total_concepts: nodes.length,
      total_edges: edges.length,
      domains,
      average_node_degree: nodes.length ? Number((edges.length * 2 / nodes.length).toFixed(2)) : 0,
      multi_course_concepts: multiCourse,
      relation_counts: relationCounts,
    },
    nodes,
    edges,
  };
}

async function loadGraphData() {
  const graphUrl = new URL("../knowledge_base/graphs/graph.json", window.location.href);
  const response = await fetch(graphUrl);
  if (response.ok) {
    return response.json();
  }

  const [nodesResponse, edgesResponse] = await Promise.all([
    fetch(new URL("../knowledge_base/graphs/nodes.json", window.location.href)),
    fetch(new URL("../knowledge_base/graphs/edges.json", window.location.href)),
  ]);
  if (!nodesResponse.ok || !edgesResponse.ok) {
    throw new Error("Unable to load graph data. Run the graph build command first.");
  }
  const [nodesPayload, edgesPayload] = await Promise.all([nodesResponse.json(), edgesResponse.json()]);
  return buildFallbackGraph(nodesPayload, edgesPayload);
}

function domainSet(graph) {
  return [...new Set(graph.nodes.map((node) => node.domain || "Other"))].sort((a, b) => a.localeCompare(b));
}

function courseSet(graph) {
  return [...new Set(graph.nodes.flatMap((node) => node.contributing_courses || []))].sort((a, b) => a.localeCompare(b));
}

function relationSet(graph) {
  return [...new Set(graph.edges.map((edge) => edge.relation_type))].sort((a, b) => a.localeCompare(b));
}

function renderLegend() {
  const domains = [
    "Machine Learning",
    "Statistics",
    "Business Analytics",
    "Data Science",
    "Leadership",
    "Communication",
    "Digital Transformation",
    "Business",
    "Project Management",
    "Soft Skills",
    "Other",
  ];
  els.legend.innerHTML = domains
    .map(
      (domain) => `
        <div class="legend-row">
          <span class="swatch" style="background:${domainColor(domain)}"></span>
          <span>${escapeHtml(domain)}</span>
        </div>`,
    )
    .join("");
}

function renderCheckboxList(container, items, selectedSet, prefix, onChange) {
  container.innerHTML = items
    .map((item) => {
      const id = `${prefix}-${normalizeText(item).replace(/[^a-z0-9]+/g, "-")}`;
      const checked = selectedSet.size === 0 || selectedSet.has(item);
      return `
        <label class="filter-option" for="${id}">
          <input id="${id}" type="checkbox" data-value="${escapeHtml(item)}" ${checked ? "checked" : ""} />
          <span>${escapeHtml(item)}</span>
        </label>`;
    })
    .join("");
  container.querySelectorAll("input[type='checkbox']").forEach((input) => {
    input.addEventListener("change", onChange);
    const value = input.dataset.value;
    if (selectedSet.size === 0) {
      selectedSet.add(value);
    }
  });
}

function updateImportanceLabel() {
  els.importanceValue.textContent = `${els.importanceRange.value}+`;
}

function visibleNodeIds() {
  const selected = state.selectedNodeId ? state.cy.$id(state.selectedNodeId) : null;
  const selectedIds = new Set();
  if (selected && selected.length) {
    selectedIds.add(selected.id());
    selected.neighborhood().forEach((ele) => {
      if (ele.isNode()) {
        selectedIds.add(ele.id());
      }
    });
  }

  const visible = new Set();
  state.cy.nodes().forEach((node) => {
    const data = node.data();
    const domainAllowed = state.filters.domains.size === 0 || state.filters.domains.has(data.domain || "Other");
    const courseAllowed =
      state.filters.courses.size === 0 ||
      (data.contributing_courses || []).some((course) => state.filters.courses.has(course));
    const importanceAllowed = Number(data.importance_score || 1) >= Number(state.filters.minImportance || 1);
    const forcedVisible = selectedIds.has(node.id());
    if ((domainAllowed && courseAllowed && importanceAllowed) || forcedVisible) {
      visible.add(node.id());
    }
  });
  return visible;
}

function visibleEdgeIds(visibleNodes) {
  const allowedRelations = state.filters.relationTypes.size === 0 ? null : state.filters.relationTypes;
  const visible = new Set();
  state.cy.edges().forEach((edge) => {
    const data = edge.data();
    const relationAllowed = !allowedRelations || allowedRelations.has(data.relation_type);
    if (relationAllowed && visibleNodes.has(data.source) && visibleNodes.has(data.target)) {
      visible.add(edge.id());
    }
  });
  return visible;
}

function updateSelectionSummary(nodeData) {
  if (!nodeData) {
    els.selectionSummary.textContent = "None";
    return;
  }
  const incoming = state.cy.edges().filter((edge) => edge.data("target") === nodeData.node_id).length;
  const outgoing = state.cy.edges().filter((edge) => edge.data("source") === nodeData.node_id).length;
  els.selectionSummary.textContent = `${incoming} incoming, ${outgoing} outgoing, ${nodeData.connected_edge_count || 0} connected`;
}

function updateStatsPanel() {
  const visibleNodes = visibleNodeIds();
  const visibleEdges = visibleEdgeIds(visibleNodes);
  const stats = state.graph.stats || {};
  const rows = [
    ["Total concepts", stats.total_concepts || 0],
    ["Total edges", stats.total_edges || 0],
    ["Visible concepts", visibleNodes.size],
    ["Visible edges", visibleEdges.size],
    ["Domains", (stats.domains || []).length],
    ["Average degree", stats.average_node_degree || 0],
    ["Multi-course", stats.multi_course_concepts || 0],
  ];
  els.stats.innerHTML = rows
    .map(([label, value]) => `<dt>${escapeHtml(label)}</dt><dd>${escapeHtml(value)}</dd>`)
    .join("");
}

function setDetailList(target, values) {
  target.innerHTML = "";
  (values || []).forEach((value) => {
    const li = document.createElement("li");
    li.textContent = value;
    target.appendChild(li);
  });
}

function setPills(target, values) {
  target.innerHTML = "";
  (values || []).forEach((value) => {
    const span = document.createElement("span");
    span.className = "meta-pill";
    span.textContent = value;
    target.appendChild(span);
  });
}

function showDetail(node) {
  const data = node.data();
  els.detailEmpty.hidden = true;
  els.detailContent.hidden = false;

  els.detailName.textContent = data.concept_name || data.node_id;
  setPills(els.detailMeta, [
    data.domain || "Other",
    data.topic || "Unknown topic",
    `Importance ${data.importance_score || 1}`,
  ]);
  els.detailDefinition.textContent = data.definition || "No definition available.";
  els.detailCore.textContent = data.core_idea || data.definition || "No core idea available.";
  els.detailInterview.textContent = data.interview_notes || "No interview notes available.";
  setDetailList(els.detailApplications, data.applications || []);
  setDetailList(els.detailRelated, [...new Set([...(data.related_concepts || []), ...(data.prerequisites || [])])]);
  setDetailList(els.detailCourses, data.contributing_courses || []);
  els.detailOpen.href = data.concept_url || "#";
  updateSelectionSummary(data);
}

function clearDetail() {
  els.detailEmpty.hidden = false;
  els.detailContent.hidden = true;
  els.selectionSummary.textContent = "None";
}

function showTooltip(node, renderedPosition) {
  const data = node.data();
  const tooltipHtml = `
    <h4>${escapeHtml(data.concept_name || data.node_id)}</h4>
    <p><strong>Domain:</strong> ${escapeHtml(data.domain || "Other")}</p>
    <p><strong>Importance:</strong> ${escapeHtml(data.importance_score || 1)}</p>
    <p><strong>Connections:</strong> ${escapeHtml(data.connected_edge_count || 0)}</p>
    <p>${escapeHtml(data.definition || "No definition available.")}</p>
  `;
  els.tooltip.innerHTML = tooltipHtml;
  els.tooltip.hidden = false;
  els.tooltip.style.left = `${renderedPosition.x + 16}px`;
  els.tooltip.style.top = `${renderedPosition.y + 16}px`;
}

function hideTooltip() {
  els.tooltip.hidden = true;
}

function applyFilterClasses() {
  const visibleNodes = visibleNodeIds();
  const visibleEdges = visibleEdgeIds(visibleNodes);
  state.cy.batch(() => {
    state.cy.nodes().forEach((node) => {
      node.toggleClass("cy-node-faded", !visibleNodes.has(node.id()));
      node.toggleClass("cy-node-search-match", state.searchResultIds.includes(node.id()));
      node.toggleClass("cy-node-selected", state.selectedNodeId === node.id());
      node.style("display", visibleNodes.has(node.id()) ? "element" : "none");
    });
    state.cy.edges().forEach((edge) => {
      edge.toggleClass("cy-edge-faded", !visibleEdges.has(edge.id()));
      edge.style("display", visibleEdges.has(edge.id()) ? "element" : "none");
    });
  });
  updateStatsPanel();
}

function layoutOptions(name) {
  const selected = state.selectedNodeId ? state.cy.$id(state.selectedNodeId) : null;
  if (name === "circle") {
    return { name: "circle", fit: true, padding: 40, animate: false, avoidOverlap: true };
  }
  if (name === "breadthfirst") {
    return {
      name: "breadthfirst",
      directed: true,
      fit: true,
      padding: 40,
      spacingFactor: 1.2,
      animate: false,
      roots: selected && selected.length ? selected : state.cy.nodes().filter((node) => Number(node.data("importance_score") || 1) >= 5).slice(0, 12),
    };
  }
  return {
    name: "cose",
    fit: true,
    padding: 40,
    animate: false,
    randomize: true,
    idealEdgeLength: 100,
    nodeRepulsion: 5000,
    nodeOverlap: 20,
    componentSpacing: 80,
    numIter: 400,
  };
}

function applyLayout(name) {
  state.layout = name;
  if (!state.cy) {
    return;
  }
  state.cy.layout(layoutOptions(name)).run();
}

function searchNodes(query) {
  const normalized = normalizeText(query);
  if (!normalized) {
    return [];
  }
  const matches = state.graph.nodes
    .map((node) => {
      const blob = normalizeText(node.search_terms?.join(" ") || nodeSearchBlob(node));
      const name = normalizeText(node.concept_name);
      const topic = normalizeText(node.topic);
      const domain = normalizeText(node.domain);
      let score = 0;
      if (name === normalized) score += 100;
      if (name.startsWith(normalized)) score += 80;
      if (blob.includes(normalized)) score += 40;
      if (topic.includes(normalized)) score += 30;
      if (domain.includes(normalized)) score += 25;
      if ((node.aliases || []).some((alias) => normalizeText(alias) === normalized)) score += 90;
      if ((node.aliases || []).some((alias) => normalizeText(alias).includes(normalized))) score += 50;
      return { node, score };
    })
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score || a.node.concept_name.localeCompare(b.node.concept_name))
    .slice(0, 10);
  return matches.map((item) => item.node);
}

function renderSearchResults(results) {
  if (!state.searchQuery.trim()) {
    els.searchResults.hidden = true;
    els.searchResults.innerHTML = "";
    state.searchResultIds = [];
    return;
  }

  state.searchResultIds = results.map((node) => node.node_id);
  els.searchResults.innerHTML = results
    .map(
      (node) => `
        <div class="search-result" role="option" data-node-id="${escapeHtml(node.node_id)}">
          <strong>${escapeHtml(node.concept_name)}</strong>
          <span>${escapeHtml(node.domain || "Other")} · ${escapeHtml(node.topic || "Unknown topic")}</span>
        </div>`,
    )
    .join("");
  els.searchResults.hidden = results.length === 0;

  els.searchResults.querySelectorAll(".search-result").forEach((item) => {
    item.addEventListener("click", () => {
      focusNode(item.dataset.nodeId, true);
      els.searchResults.hidden = true;
    });
  });
}

function focusNode(nodeId, shouldPan = true) {
  const node = state.cy.$id(nodeId);
  if (!node || !node.length) {
    return;
  }
  state.selectedNodeId = nodeId;
  showDetail(node);
  applyFilterClasses();
  if (shouldPan) {
    const neighborhood = node.closedNeighborhood();
    state.cy.animate(
      {
        fit: {
          eles: neighborhood,
          padding: 120,
        },
      },
      { duration: 220 },
    );
  }
}

function clearSelection() {
  state.selectedNodeId = "";
  clearDetail();
  applyFilterClasses();
}

function renderFilters() {
  const domains = domainSet(state.graph);
  const courses = courseSet(state.graph);
  const relations = relationSet(state.graph);
  state.filters.domains = new Set(domains);
  state.filters.courses = new Set(courses);
  state.filters.relationTypes = new Set(relations);

  renderCheckboxList(els.domainFilters, domains, state.filters.domains, "domain", () => {
    state.filters.domains = new Set(
      [...els.domainFilters.querySelectorAll("input[type='checkbox']")]
        .filter((input) => input.checked)
        .map((input) => input.dataset.value),
    );
    applyFilterClasses();
  });

  renderCheckboxList(els.courseFilters, courses, state.filters.courses, "course", () => {
    state.filters.courses = new Set(
      [...els.courseFilters.querySelectorAll("input[type='checkbox']")]
        .filter((input) => input.checked)
        .map((input) => input.dataset.value),
    );
    applyFilterClasses();
  });

  renderCheckboxList(els.relationFilters, relations, state.filters.relationTypes, "relation", () => {
    state.filters.relationTypes = new Set(
      [...els.relationFilters.querySelectorAll("input[type='checkbox']")]
        .filter((input) => input.checked)
        .map((input) => input.dataset.value),
    );
    applyFilterClasses();
  });
}

function createCy() {
  const elements = [
    ...state.graph.nodes.map((node) => ({
      data: {
        id: node.node_id,
        label: node.concept_name,
        concept_name: node.concept_name,
        concept_key: node.concept_key,
        domain: node.domain || "Other",
        topic: node.topic || "",
        importance_score: Number(node.importance_score || 1),
        contributing_courses: node.contributing_courses || [],
        contributing_lecture_files: node.contributing_lecture_files || [],
        aliases: node.aliases || [],
        prerequisites: node.prerequisites || [],
        related_concepts: node.related_concepts || [],
        broader_topics: node.broader_topics || [],
        applications: node.applications || [],
        definition: node.definition || "",
        core_idea: node.core_idea || "",
        interview_notes: node.interview_notes || "",
        connected_edge_count: Number(node.connected_edge_count || 0),
        degree: Number(node.degree || 0),
        metadata_path: node.metadata_path || "",
        metadata_url: node.metadata_url || siteUrlFromMetadataPath(node.metadata_path, "metadata.json"),
        concept_url: node.concept_url || conceptViewerUrl(node.metadata_path),
        search_terms: node.search_terms || [],
      },
    })),
    ...state.graph.edges.map((edge) => ({
      data: {
        id: edge.edge_id,
        source: edge.source,
        target: edge.target,
        relation_type: edge.relation_type,
        source_concept_key: edge.source_concept_key,
        target_concept_key: edge.target_concept_key,
        source_concept_name: edge.source_concept_name,
        target_concept_name: edge.target_concept_name,
        target_resolved: Boolean(edge.target_resolved),
      },
      classes: `edge-${edge.relation_type || "related"}`,
    })),
  ];

  const styles = [
    {
      selector: "core",
      style: {
        "background-color": "#f4f6f9",
        "selection-box-color": "#315efb",
        "selection-box-opacity": 0.12,
        "active-bg-opacity": 0.08,
      },
    },
    {
      selector: "node",
      style: {
        label: "data(label)",
        color: "#ffffff",
        "font-size": 10,
        "font-weight": 600,
        "text-wrap": "wrap",
        "text-max-width": 88,
        "text-valign": "center",
        "text-halign": "center",
        "background-color": "data(domainColor)",
        "border-width": 1.5,
        "border-color": "rgba(17, 24, 39, 0.18)",
        width: "mapData(importance_score, 1, 5, 28, 66)",
        height: "mapData(importance_score, 1, 5, 28, 66)",
        "text-outline-color": "rgba(17, 24, 39, 0.28)",
        "text-outline-width": 2,
      },
    },
    {
      selector: "edge",
      style: {
        width: 1.5,
        "line-color": "#94a3b8",
        "target-arrow-color": "#94a3b8",
        "source-arrow-color": "#94a3b8",
        "curve-style": "bezier",
        "target-arrow-shape": "triangle",
        opacity: 0.8,
      },
    },
    {
      selector: ".edge-prerequisite",
      style: {
        "line-color": "#2563eb",
        "target-arrow-color": "#2563eb",
        width: 2,
      },
    },
    {
      selector: ".edge-related",
      style: {
        "line-style": "dashed",
        "target-arrow-shape": "none",
        "line-color": "#64748b",
      },
    },
    {
      selector: ".edge-broader",
      style: {
        "line-color": "#f97316",
        "target-arrow-color": "#f97316",
        width: 2,
      },
    },
    {
      selector: ".edge-used_in",
      style: {
        "line-color": "#8b5cf6",
        "target-arrow-color": "#8b5cf6",
      },
    },
    {
      selector: ".edge-application",
      style: {
        "line-color": "#10b981",
        "target-arrow-color": "#10b981",
        "line-style": "dotted",
      },
    },
    {
      selector: ".cy-node-selected",
      style: {
        "border-color": "#111827",
        "border-width": 4,
      },
    },
    {
      selector: ".cy-node-search-match",
      style: {
        "border-color": "#111827",
        "border-width": 3,
      },
    },
    {
      selector: ".cy-node-faded",
      style: {
        opacity: 0.14,
      },
    },
    {
      selector: ".cy-edge-faded",
      style: {
        opacity: 0.08,
      },
    },
    {
      selector: ".cy-filtered-out",
      style: {
        display: "none",
      },
    },
  ];

  state.cy = cytoscape({
    container: els.graph,
    elements,
    style: styles,
    wheelSensitivity: 0.2,
    minZoom: 0.1,
    maxZoom: 2.5,
    hideEdgesOnViewport: true,
    textureOnViewport: true,
    motionBlur: true,
  });

  state.cy.nodes().forEach((node) => {
    node.data("domainColor", domainColor(node.data("domain")));
  });

  state.cy.on("tap", "node", (evt) => {
    focusNode(evt.target.id(), false);
  });

  state.cy.on("tap", (evt) => {
    if (evt.target === state.cy) {
      clearSelection();
    }
  });

  state.cy.on("mouseover", "node", (evt) => {
    showTooltip(evt.target, evt.renderedPosition);
  });

  state.cy.on("mousemove", "node", (evt) => {
    if (!els.tooltip.hidden) {
      showTooltip(evt.target, evt.renderedPosition);
    }
  });

  state.cy.on("mouseout", "node", () => {
    hideTooltip();
  });

  applyLayout(state.layout);
}

function wireControls() {
  els.searchInput.addEventListener("input", () => {
    state.searchQuery = els.searchInput.value;
    const results = searchNodes(state.searchQuery);
    renderSearchResults(results);
    applyFilterClasses();
  });

  els.searchInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      const results = searchNodes(state.searchQuery);
      if (results.length) {
        focusNode(results[0].node_id, true);
        els.searchResults.hidden = true;
      }
    }
    if (event.key === "Escape") {
      els.searchResults.hidden = true;
      els.searchInput.blur();
    }
  });

  els.layoutSelect.addEventListener("change", () => {
    applyLayout(els.layoutSelect.value);
  });

  els.fitBtn.addEventListener("click", () => {
    state.cy.fit(state.cy.elements(":visible"), 40);
  });

  els.resetBtn.addEventListener("click", () => {
    state.filters.minImportance = 1;
    state.selectedNodeId = "";
    state.searchQuery = "";
    els.searchInput.value = "";
    els.importanceRange.value = "1";
    updateImportanceLabel();
    renderFilters();
    clearSelection();
    renderSearchResults([]);
    applyLayout(els.layoutSelect.value);
    state.cy.fit(state.cy.elements(":visible"), 40);
  });

  els.importanceRange.addEventListener("input", () => {
    state.filters.minImportance = Number(els.importanceRange.value);
    updateImportanceLabel();
    applyFilterClasses();
  });

  document.addEventListener("click", (event) => {
    if (!els.searchResults.contains(event.target) && event.target !== els.searchInput) {
      els.searchResults.hidden = true;
    }
  });
}

async function init() {
  renderLegend();
  updateImportanceLabel();
  state.graph = await loadGraphData();
  renderFilters();
  createCy();
  wireControls();
  updateStatsPanel();
  clearDetail();
  state.cy.fit(state.cy.elements(":visible"), 40);
}

init().catch((error) => {
  console.error(error);
  els.graph.innerHTML = `<div class="empty-state" style="padding:1rem;color:#b91c1c;">${escapeHtml(error.message || "Failed to load graph data.")}</div>`;
});
