/** Pure graph presentation consumer. No DOM, topology generation, or fallback. */
export class GraphContractError extends Error {
  constructor(issues) {
    super(issues.map(i => `${i.location}: ${i.message}`).join('; '));
    this.issues = issues;
  }
}
function fail(code, location, message) {
  throw new GraphContractError([{code, location, message}]);
}
function decodedPath(url, location) {
  try { return decodeURIComponent(url.pathname); }
  catch { fail('published_path', location, 'Malformed URL escaping'); }
}
function below(path, root) { return path.startsWith(root.endsWith('/') ? root : root + '/'); }
function settings(options) {
  const base = new URL(options.baseUrl);
  if (!['http:', 'https:'].includes(base.protocol)) fail('published_path', 'baseUrl', 'Expected HTTP site URL');
  function configured(value, fallback, name, directory = false) {
    const url = new URL(value ?? fallback, base);
    if (url.origin !== base.origin || url.hash || (name !== 'graphUrl' && url.search)) fail('published_path', name, 'Expected same-origin site URL');
    if (directory && !url.pathname.endsWith('/')) url.pathname += '/';
    decodedPath(url, name);
    return url;
  }
  const repo = configured(options.repoRootUrl, '../', 'repoRootUrl', true);
  const refined = configured(options.refinedRootUrl, '../knowledge_base/refined/', 'refinedRootUrl', true);
  const viewer = configured(options.viewerUrl, './concept.html', 'viewerUrl');
  const graph = configured(options.graphUrl, '../knowledge_base/graphs/graph.json', 'graphUrl');
  if (!below(decodedPath(refined, 'refinedRootUrl'), decodedPath(repo, 'repoRootUrl')))
    fail('published_path', 'refinedRootUrl', 'Refined root outside repository');
  return {base, repo, refined, viewer, graph};
}
function relative(raw, location) {
  if (typeof raw !== 'string' || !raw || /^[a-z][a-z0-9+.-]*:/i.test(raw) || raw.startsWith('/') ||
      /[\\\x00-\x1f\x7f]/.test(raw) || /%(?![0-9a-f]{2})|%(?:2f|5c)/i.test(raw))
    fail('published_path', location, 'Expected safe relative URL');
  for (const segment of raw.split(/[/?#]/)) {
    if (segment.includes('%')) {
      let value;
      try { value = decodeURIComponent(segment); } catch { fail('published_path', location, 'Malformed escaping'); }
      if (value === '.' || value === '..') fail('published_path', location, 'Encoded traversal');
    }
  }
}
function resource(raw, config, filename, location) {
  relative(raw, location);
  const url = new URL(raw, config.base);
  const pathname = decodedPath(url, location);
  if (url.origin !== config.base.origin || url.search || url.hash || /[\\\x00-\x1f\x7f]/.test(pathname) ||
      !below(pathname, decodedPath(config.refined, location)) || !pathname.endsWith('/' + filename))
    fail('published_path', location, 'Resource outside published concept root or wrong filename');
  return url;
}
export function resolveConceptPath(rawPath, options) {
  return resource(rawPath, settings(options), 'concept.md', 'concept_path');
}
function validateUrls(node, config, version, location) {
  const metadata = resource(node.metadata_url, config, 'metadata.json', location + '/metadata_url');
  if (/[\\\x00-\x1f\x7f]|%(?![0-9a-f]{2})/i.test(node.concept_url)) fail('published_path', location + '/concept_url', 'Invalid viewer URL');
  relative(node.concept_url.split('?')[0], location + '/concept_url');
  const viewer = new URL(node.concept_url, config.base);
  if (viewer.origin !== config.viewer.origin || viewer.pathname !== config.viewer.pathname || viewer.hash ||
      viewer.searchParams.getAll('path').length !== 1 ||
      [...viewer.searchParams.keys()].some(k => !((version === 1 ? ['path', 'view'] : ['path']).includes(k))))
    fail('published_path', location + '/concept_url', 'Expected viewer with exactly one path query');
  const markdown = resource(viewer.searchParams.get('path'), config, 'concept.md', location + '/concept_url');
  if (decodedPath(metadata, location).replace(/metadata\.json$/, '') !== decodedPath(markdown, location).replace(/concept\.md$/, ''))
    fail('published_path', location + '/concept_url', 'Metadata and concept targets disagree');
  const canonical = decodedPath(metadata, location).slice(decodedPath(config.repo, location).length);
  if (version === 1) node.metadata_path = canonical;
  else if (node.metadata_path !== canonical || node.metadata_path.split('/').includes('..') || /[\\\x00-\x1f\x7f]/.test(node.metadata_path))
    fail('published_path', location + '/metadata_path', 'Metadata path/URL disagree');
}
function object(v) { return v !== null && typeof v === 'object' && !Array.isArray(v); }
function stringList(v) { return Array.isArray(v) && v.every(x => typeof x === 'string'); }
function jsonValue(v, active = new Set()) {
  if (v === null || typeof v === 'string' || typeof v === 'boolean') return true;
  if (typeof v === 'number') return Number.isFinite(v);
  if (typeof v !== 'object' || active.has(v)) return false;
  if (!Array.isArray(v) && Object.getPrototypeOf(v) !== Object.prototype && Object.getPrototypeOf(v) !== null) return false;
  active.add(v);
  const result = Object.values(v).every(x => jsonValue(x, active));
  active.delete(v);
  return result;
}
function timestamp(s) {
  if (typeof s !== 'string') return false;
  const m = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d{1,6})?(Z|[+-](\d{2}):(\d{2}))$/.exec(s);
  if (!m) return false;
  const [y, mo, d, h, mi, sec] = m.slice(1, 7).map(Number);
  const days = [31, (y % 4 === 0 && (y % 100 !== 0 || y % 400 === 0)) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  return y >= 1 && mo >= 1 && mo <= 12 && d >= 1 && d <= days[mo - 1] && h < 24 && mi < 60 && sec < 60 &&
    (m[7] === 'Z' || (Number(m[8]) < 24 && Number(m[9]) < 60));
}
function codepointCompare(a, b) {
  const x = [...a].map(c => c.codePointAt(0)), y = [...b].map(c => c.codePointAt(0));
  for (let i = 0; i < Math.min(x.length, y.length); i++) if (x[i] !== y[i]) return x[i] - y[i];
  return x.length - y.length;
}
const nodeLists = ['contributing_courses','contributing_lecture_files','aliases','prerequisites','related_concepts','broader_topics','applications','search_terms'];
const ranks = ['importance_score','scope_level','study_priority'];
const counts = ['degree','connected_edge_count'];
const nodeStrings = ['node_id','concept_key','concept_name','domain','topic','definition','core_idea','interview_notes','metadata_path','metadata_url','concept_url'];
const requiredText = ['node_id','concept_key','concept_name','metadata_path','metadata_url','concept_url'];
const edgeStrings = ['edge_id','source','target','relation_type','source_concept_key','target_concept_key','source_concept_name','target_concept_name'];

export function validateGraphPayload(payload, options) {
  const config = settings(options);
  if (!object(payload)) fail('field_type', '/', 'Expected graph object');
  const version = payload.schema_version;
  if (!Number.isInteger(version) || ![1,2].includes(version)) fail('schema_version', '/schema_version', 'Unsupported graph schema version');
  if (!timestamp(payload.generated_at)) fail('timestamp', '/generated_at', 'Expected valid timezone-bearing ISO timestamp');
  if (!jsonValue(payload)) fail('field_type', '/', 'Graph must contain finite JSON values');
  const graph = structuredClone(payload);
  for (const k of ['nodes','edges']) if (!Array.isArray(graph[k])) fail('field_type', '/' + k, 'Expected list');
  const ids = new Set(), keys = new Set(), nodes = new Map();
  graph.nodes.forEach((n, i) => {
    const loc = `/nodes/${i}`;
    if (!object(n)) fail('field_type', loc, 'Expected node object');
    for (const k of nodeStrings) if (typeof n[k] !== 'string' || (requiredText.includes(k) && !n[k].trim())) fail('field_type', loc + '/' + k, 'Invalid/missing node field');
    for (const k of nodeLists) if (!stringList(n[k])) fail('field_type', loc + '/' + k, 'Expected string list');
    for (const k of ranks) if (!Number.isInteger(n[k]) || n[k] < 1 || n[k] > 5) fail('field_type', loc + '/' + k, 'Invalid rank');
    for (const k of counts) if (!Number.isInteger(n[k]) || n[k] < 0) fail('field_type', loc + '/' + k, 'Invalid count');
    if (ids.has(n.node_id)) fail('duplicate_id', loc + '/node_id', 'Duplicate node ID');
    if (keys.has(n.concept_key)) fail('duplicate_key', loc + '/concept_key', 'Duplicate concept key');
    ids.add(n.node_id); keys.add(n.concept_key); nodes.set(n.node_id, n);
    validateUrls(n, config, version, loc);
  });
  const degrees = new Map(), relations = new Map();
  graph.edges.forEach((e, i) => {
    const loc = `/edges/${i}`;
    if (!object(e)) fail('field_type', loc, 'Expected edge object');
    for (const k of edgeStrings) if (typeof e[k] !== 'string' || !e[k].trim()) fail('field_type', loc + '/' + k, 'Invalid/missing edge field');
    for (const k of ['supporting_courses','supporting_lecture_files']) if (!stringList(e[k])) fail('field_type', loc + '/' + k, 'Expected string list');
    if (!object(e.supporting_lecture_hashes) || !Object.values(e.supporting_lecture_hashes).every(v => typeof v === 'string')) fail('field_type', loc + '/supporting_lecture_hashes', 'Expected hash map');
    if (typeof e.target_resolved !== 'boolean') fail('field_type', loc + '/target_resolved', 'Expected boolean');
    if (ids.has(e.edge_id)) fail('duplicate_id', loc + '/edge_id', 'Duplicate graph ID');
    ids.add(e.edge_id);
    if (!nodes.has(e.source) || !nodes.has(e.target)) fail('dangling_endpoint', loc, 'Missing edge endpoint');
    if (e.source === e.target) fail('self_edge', loc, 'Self edge not supported');
    if (['source','target'].some(k => e[k + '_concept_key'] !== nodes.get(e[k]).concept_key)) fail('endpoint_key', loc, 'Endpoint key mismatch');
    if (!e.target_resolved) fail('unresolved_edge', loc, 'Unresolved edge');
    if (!['prerequisite','related'].includes(e.relation_type)) fail('relation_type', loc, 'Unsupported relation');
    for (const id of [e.source,e.target]) degrees.set(id, (degrees.get(id) || 0) + 1);
    relations.set(e.relation_type, (relations.get(e.relation_type) || 0) + 1);
  });
  graph.nodes.forEach((n,i) => {
    if (n.degree !== (degrees.get(n.node_id) || 0) || n.connected_edge_count !== (degrees.get(n.node_id) || 0)) fail('node_degree', `/nodes/${i}`, 'Incident edge count mismatch');
  });
  const n = graph.nodes.length, e = graph.edges.length;
  const expected = {
    total_concepts:n, total_edges:e,
    domains:[...new Set(graph.nodes.map(v=>v.domain).filter(v=>v.trim()))].sort(codepointCompare),
    average_node_degree:n ? Math.floor((400*e+n)/(2*n))/100 : 0,
    multi_course_concepts:graph.nodes.filter(v=>new Set(v.contributing_courses).size>1).length,
    relation_counts:Object.fromEntries([...relations].sort(([a],[b])=>codepointCompare(a,b))),
  };
  if (!object(graph.stats)) fail('field_type', '/stats', 'Expected stats object');
  for (const [k,v] of Object.entries(expected)) {
    const actual = graph.stats[k];
    const same = Array.isArray(v) ? stringList(actual) && actual.length === v.length && actual.every((x,i)=>x===v[i]) :
      object(v) ? object(actual) && Object.keys(actual).length === Object.keys(v).length && Object.entries(v).every(([key,value])=>actual[key]===value) :
      typeof actual === 'number' && actual === v;
    if (!same) fail('stats', '/stats/' + k, 'Statistics mismatch');
  }
  return graph;
}
export async function loadGraphData(options, fetcher = globalThis.fetch) {
  try {
    const response = await fetcher(settings(options).graph);
    if (!response.ok) fail('io_error', 'graph.json', `Unable to load graph bundle (${response.status})`);
    return validateGraphPayload(await response.json(), options);
  } catch (error) {
    if (error instanceof GraphContractError) throw error;
    fail('io_error', 'graph.json', error.message || 'Unable to load graph bundle');
  }
}
