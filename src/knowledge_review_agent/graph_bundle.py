from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .concept_document import parse_concept_document, canonical_section_name
from .models import ConceptMetadata, GraphEdge, GraphNode
from .utils import normalize_concept_key, normalize_spaces


@dataclass(frozen=True)
class GraphBundleNode:
    node_id: str
    concept_key: str
    concept_name: str
    domain: str
    topic: str
    importance_score: int
    scope_level: int
    study_priority: int
    contributing_courses: list[str]
    contributing_lecture_files: list[str]
    aliases: list[str]
    prerequisites: list[str]
    related_concepts: list[str]
    broader_topics: list[str]
    applications: list[str]
    definition: str
    core_idea: str
    interview_notes: str
    connected_edge_count: int
    degree: int
    metadata_path: str
    metadata_url: str
    concept_url: str
    search_terms: list[str]


@dataclass(frozen=True)
class GraphBundleEdge:
    edge_id: str
    source: str
    target: str
    relation_type: str
    source_concept_key: str
    target_concept_key: str
    source_concept_name: str
    target_concept_name: str
    target_resolved: bool
    supporting_courses: list[str]
    supporting_lecture_files: list[str]
    supporting_lecture_hashes: dict[str, str]


@dataclass
class GraphBundle:
    generated_at: str
    schema_version: int = 2
    stats: dict[str, object] = field(default_factory=dict)
    nodes: list[GraphBundleNode] = field(default_factory=list)
    edges: list[GraphBundleEdge] = field(default_factory=list)


def _default_paths():
    root = Path(__file__).resolve().parents[2]
    return GraphPresentationPaths(root, root/"knowledge_base/concepts", root/"knowledge_base/refined", root/"website")


def _published_record(node, paths):
    from dataclasses import fields
    raw_path = Path(node.metadata_path)
    raw_path = raw_path if raw_path.is_absolute() else paths.repo_root/raw_path
    if raw_path.name != "metadata.json": _fail("refined_record",node.node_id,"Expected metadata.json")
    for root in (paths.concepts_root, paths.refined_root):
        if raw_path.absolute().is_relative_to(root.absolute()):
            _guard_path(raw_path,root,node.node_id)
            relative = raw_path.absolute().relative_to(root.absolute())
            break
    else: _fail("refined_record",node.node_id,"Node metadata outside declared roots")
    metadata_path = paths.refined_root/relative
    markdown_path = metadata_path.with_name("concept.md")
    for path in (metadata_path,markdown_path):
        _guard_path(path,paths.refined_root,str(path))
    try:
        payload = json.loads(metadata_path.read_bytes())
        json.dumps(payload, allow_nan=False)
        if not isinstance(payload,dict): raise ValueError("Metadata must be object")
        defaults = ConceptMetadata(concept_name="")
        values = {}
        for spec in fields(defaults):
            if spec.name not in payload: continue
            value,default = payload[spec.name],getattr(defaults,spec.name)
            if isinstance(default,str): valid=isinstance(value,str)
            elif isinstance(default,int): valid=type(value) is int
            elif isinstance(default,float): valid=type(value) in {int,float}
            elif isinstance(default,list): valid=isinstance(value,list) and (spec.name=="persistence_conflicts" or all(isinstance(v,str) for v in value))
            elif isinstance(default,dict): valid=isinstance(value,dict) and all(isinstance(k,str) and isinstance(v,str) for k,v in value.items())
            else: valid=True
            if not valid: raise ValueError("Invalid metadata field: "+spec.name)
            values[spec.name]=value
        metadata = ConceptMetadata(**values)
        document = parse_concept_document(markdown_path.read_bytes().decode("utf-8"))
    except (OSError,ValueError,TypeError,KeyError) as exc: _fail("refined_record",str(metadata_path),str(exc))
    expected = {"concept_key":metadata.canonical_key or normalize_concept_key(metadata.concept_name),
        "concept_name":metadata.concept_name,"version_number":metadata.version_number,
        "last_updated_timestamp":metadata.last_updated_timestamp,"domain":metadata.domain,"topic":metadata.topic,
        "importance_score":metadata.importance_score,"scope_level":metadata.scope_level,"study_priority":metadata.study_priority,
        "contributing_courses":metadata.contributing_courses,"contributing_lecture_files":metadata.contributing_lecture_files}
    for name,value in expected.items():
        actual=getattr(node,name)
        if (set(actual)!=set(value) if isinstance(value,list) else actual!=value):
            _fail("node_metadata_mismatch",node.node_id+"/"+name,"Topology disagrees with refined metadata")
    return metadata_path,markdown_path,metadata,document


def _load_node_bundle(node, paths):
    import os
    from urllib.parse import quote
    metadata_path,markdown_path,metadata,document = _published_record(node,paths)
    def selected(*names):
        for name in names:
            bodies=[s.content.strip("\n") for s in document.sections if canonical_section_name(s.heading)==name and s.content.strip()]
            if bodies: return "\n\n".join(bodies)
        return ""
    def unique(items): return sorted(set(v for v in items if v.strip()))
    lists={name:unique(getattr(metadata,name)) for name in
           ("contributing_courses","contributing_lecture_files","aliases","prerequisites","related_concepts","broader_topics","applications")}
    lists["aliases"]=unique([*lists["aliases"],metadata.concept_name])
    metadata_url=quote(os.path.relpath(metadata_path,paths.website_root).replace(os.sep,"/"),safe="/")
    resource=quote(os.path.relpath(markdown_path,paths.website_root).replace(os.sep,"/"),safe="/")
    payload={name:getattr(node,name) for name in ("node_id","concept_key","concept_name","domain","topic","importance_score","scope_level","study_priority")}
    payload.update(lists,definition=metadata.definition,
        core_idea=selected("Core Intuition","Why it Matters") or metadata.intuition or metadata.definition,
        interview_notes=selected("Interview Questions","Common Mistakes"),degree=0,connected_edge_count=0,
        metadata_path=metadata_path.resolve().relative_to(paths.repo_root.resolve()).as_posix(), metadata_url=metadata_url,
        concept_url="./concept.html?path="+quote(resource,safe=""))
    payload["search_terms"]=unique([node.concept_name,node.concept_key,node.domain,node.topic,*[v for values in lists.values() for v in values]])
    return payload


def _load_edge_bundle(edge):
    return {"edge_id":edge.edge_id,"source":edge.source_node_id,"target":edge.target_node_id,"relation_type":edge.relation_type,
        "source_concept_key":edge.source_concept_key,"target_concept_key":edge.target_concept_key,
        "source_concept_name":edge.source_concept_name,"target_concept_name":edge.target_concept_name,"target_resolved":edge.target_resolved,
        "supporting_courses":sorted(set(edge.supporting_courses)),"supporting_lecture_files":sorted(set(edge.supporting_lecture_files)),
        "supporting_lecture_hashes":dict(sorted(edge.supporting_lecture_hashes.items()))}


def build_graph_bundle(nodes: list[GraphNode], edges: list[GraphEdge], graphs_root: Path, generated_at: str, *, paths: GraphPresentationPaths | None = None) -> GraphBundle:
    from dataclasses import asdict
    paths=paths or _default_paths()
    validate_graph_paths(paths,graphs_root=graphs_root)
    node_payloads=[_load_node_bundle(n,paths) for n in sorted(nodes,key=lambda n:n.node_id)]
    edge_payloads=[_load_edge_bundle(e) for e in sorted(edges,key=lambda e:e.edge_id)]
    degree=Counter(v for e in edge_payloads for v in (e['source'],e['target']))
    for n in node_payloads:n.update(degree=degree[n['node_id']],connected_edge_count=degree[n['node_id']])
    n,e=len(node_payloads),len(edge_payloads)
    stats=dict(total_concepts=n,total_edges=e,domains=sorted({v['domain'] for v in node_payloads if v['domain'].strip()}),
        average_node_degree=((400*e+n)//(2*n))/100 if n else 0,
        multi_course_concepts=sum(len(v['contributing_courses'])>1 for v in node_payloads),relation_counts=dict(sorted(Counter(v['relation_type'] for v in edge_payloads).items())))
    bundle=GraphBundle(generated_at,stats=stats,nodes=[GraphBundleNode(**v) for v in node_payloads],edges=[GraphBundleEdge(**v) for v in edge_payloads])
    validate_graph_payload(asdict(bundle),paths=paths,check_files=True)
    return bundle


def write_graph_bundle(graphs_root: Path, nodes: list[GraphNode], edges: list[GraphEdge], generated_at: str, *, paths: GraphPresentationPaths | None = None) -> Path:
    import os
    import stat
    import tempfile
    from dataclasses import asdict
    paths=paths or _default_paths()
    payload=asdict(build_graph_bundle(nodes,edges,graphs_root,generated_at,paths=paths))
    graph_json=graphs_root/'graph.json'
    def semantic(v):return {k:value for k,value in v.items() if k!='generated_at'}
    if graph_json.exists():
        try:
            old=load_graph_bundle(graph_json,paths=paths)
            if semantic(old)==semantic(payload):return graph_json
        except GraphContractError as exc:
            if any(i.code in {'io_error','unsafe_output'} for i in exc.issues):raise
    temporary=None
    try:
        graphs_root.mkdir(parents=True,exist_ok=True)
        mode = stat.S_IMODE(graph_json.stat().st_mode) if graph_json.exists() else 0o644
        fd,temporary=tempfile.mkstemp(prefix='.graph-',dir=graphs_root)
        with os.fdopen(fd,'w',encoding='utf-8') as stream:
            stream.write(json.dumps(payload,indent=2,ensure_ascii=True,sort_keys=True,allow_nan=False))
            os.fchmod(stream.fileno(), mode)
            stream.flush();os.fsync(stream.fileno())
        os.replace(temporary,graph_json)
    except (OSError,ValueError) as exc: _fail('io_error',str(graph_json),str(exc))
    finally:
        if temporary and os.path.exists(temporary):os.unlink(temporary)
    return graph_json


# Presentation validation is independent of graph generation and filesystem layout.
@dataclass(frozen=True)
class GraphPresentationPaths:
    repo_root: Path
    concepts_root: Path
    refined_root: Path
    website_root: Path


@dataclass(frozen=True)
class GraphContractIssue:
    code: str
    location: str
    message: str


class GraphContractError(ValueError):
    def __init__(self, issues: tuple[GraphContractIssue, ...]):
        self.issues = issues
        super().__init__('; '.join(f'{i.location}: {i.message}' for i in issues))


def _fail(code, location, message):
    raise GraphContractError((GraphContractIssue(code, location, message),))


def _guard_path(path: Path, root: Path, location: str, code='published_path') -> Path:
    try:
        relative = path.absolute().relative_to(root.absolute())
        if '..' in relative.parts or root.is_symlink():
            raise ValueError('Unsafe path')
        cursor = root
        for part in relative.parts:
            cursor /= part
            if cursor.is_symlink(): raise ValueError('Symlink path')
        resolved = path.resolve()
        if not resolved.is_relative_to(root.resolve()): raise ValueError('Path escapes root')
        return resolved
    except (OSError, ValueError) as exc:
        _fail(code, location, str(exc))


def validate_graph_paths(paths: GraphPresentationPaths, *, graphs_root: Path | None = None) -> None:
    for name in ('concepts_root', 'refined_root', 'website_root'):
        _guard_path(getattr(paths, name), paths.repo_root, name)
    a, b = paths.concepts_root.resolve(), paths.refined_root.resolve()
    if a.is_relative_to(b) or b.is_relative_to(a):
        _fail('published_path', 'roots', 'Draft and refined roots must not overlap')
    if graphs_root is not None:
        # Preserve system aliases above declared roots, but never follow an
        # output redirect inside the selected repository.
        if graphs_root.absolute().is_relative_to(paths.repo_root.absolute()):
            _guard_path(graphs_root, paths.repo_root, str(graphs_root), code='unsafe_output')
        for target in (graphs_root, graphs_root/'graph.json'):
            if target.is_symlink(): _fail('unsafe_output', str(target), 'Symlink output')
        output = graphs_root.resolve()
        if any(output.is_relative_to(r) or r.is_relative_to(output) for r in (a, b)):
            _fail('unsafe_output', str(graphs_root), 'Graph output overlaps concept inputs')


def _resource_path(raw, paths, filename, location):
    from urllib.parse import urlsplit, urljoin, unquote, quote
    if (not isinstance(raw, str) or not raw or re.search(r'[\\\x00-\x20]', raw.replace(' ', ''))
            or re.search(r'%(?![0-9a-fA-F]{2})|%(?:2f|5c)', raw, re.I)):
        _fail('published_path', location, 'Invalid published resource URL')
    split = urlsplit(raw)
    if split.scheme or split.netloc or split.path.startswith('/') or split.query or split.fragment:
        _fail('published_path', location, 'Expected relative published URL without query or fragment')
    base = 'https://graph.invalid/' + quote(paths.website_root.resolve().relative_to(paths.repo_root.resolve()).as_posix(), safe='/') + '/index.html'
    joined = urlsplit(urljoin(base, raw))
    try:
        decoded = unquote(joined.path, errors='strict')
        if '\\' in decoded or re.search(r'[\x00-\x1f\x7f]', decoded): raise ValueError('Unsafe decoded path')
        target = paths.repo_root / decoded.lstrip('/')
        target = _guard_path(target, paths.refined_root, location)
    except (ValueError, UnicodeError) as exc:
        _fail('published_path', location, str(exc))
    if target.name != filename:
        _fail('published_path', location, f'Expected {filename}')
    return target


def _validate_node_urls(node, paths, version, location, check_files):
    from urllib.parse import urlsplit, parse_qsl, urljoin, quote
    metadata = _resource_path(node['metadata_url'], paths, 'metadata.json', location+'/metadata_url')
    raw = node['concept_url']
    if re.search(r'[\\\x00-\x1f\x7f]|%(?![0-9a-fA-F]{2})', raw):
        _fail('published_path', location+'/concept_url', 'Invalid viewer URL')
    url = urlsplit(raw)
    if url.scheme or url.netloc or url.path.startswith('/') or url.fragment:
        _fail('published_path', location+'/concept_url', 'Expected relative concept viewer')
    website_relative = paths.website_root.resolve().relative_to(paths.repo_root.resolve()).as_posix()
    base = 'https://graph.invalid/' + quote(website_relative, safe='/') + '/index.html'
    if urljoin(base, url.path) != urljoin(base, './concept.html'):
        _fail('published_path', location+'/concept_url', 'Unexpected viewer path')
    query = parse_qsl(url.query, keep_blank_values=True)
    if (len([v for k,v in query if k == 'path']) != 1 or
            any(k not in ({'path','view'} if version == 1 else {'path'}) for k,v in query)):
        _fail('published_path', location+'/concept_url', 'Expected exactly one path query')
    markdown = _resource_path(next(v for k,v in query if k == 'path'), paths, 'concept.md', location+'/concept_url')
    if markdown.parent != metadata.parent:
        _fail('published_path', location+'/concept_url', 'Metadata and concept targets disagree')
    if version == 1:
        node['metadata_path'] = metadata.relative_to(paths.repo_root.resolve()).as_posix()
    else:
        raw_path = node['metadata_path']
        if Path(raw_path).is_absolute() or '\\' in raw_path or '..' in Path(raw_path).parts:
            _fail('published_path', location+'/metadata_path', 'Expected repo-relative refined metadata path')
        if _guard_path(paths.repo_root/raw_path, paths.refined_root, location+'/metadata_path') != metadata:
            _fail('published_path', location+'/metadata_path', 'Metadata path/URL disagree')
    if check_files:
        for file in (metadata, markdown, paths.website_root/'concept.html'):
            if not file.is_file() or file.is_symlink():
                _fail('refined_record', str(file), 'Missing regular published file')


def validate_graph_payload(payload: object, *, paths: GraphPresentationPaths, check_files: bool = False) -> dict:
    import copy
    import math
    from dataclasses import fields
    from datetime import datetime
    validate_graph_paths(paths)
    if not isinstance(payload, dict): _fail('field_type', '/', 'Expected graph object')
    version = payload.get('schema_version')
    if type(version) is not int or version not in (1,2): _fail('schema_version', '/schema_version', 'Unsupported graph schema version')
    stamp = payload.get('generated_at')
    try:
        if not isinstance(stamp, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})', stamp): raise ValueError()
        offset = re.search(r'([+-])(\d{2}):(\d{2})$', stamp)
        if offset and (int(offset[2]) >= 24 or int(offset[3]) >= 60): raise ValueError()
        datetime.fromisoformat(stamp.replace('Z', '+00:00'))
    except ValueError: _fail('timestamp', '/generated_at', 'Expected valid timezone-bearing ISO timestamp')
    try: json.dumps(payload, allow_nan=False)
    except (ValueError, TypeError): _fail('field_type', '/', 'Graph must contain finite JSON values')
    result = copy.deepcopy(payload)
    for name in ('nodes','edges'):
        if not isinstance(result.get(name), list): _fail('field_type', '/'+name, 'Expected list')
    node_lists = {'contributing_courses','contributing_lecture_files','aliases','prerequisites','related_concepts','broader_topics','applications','search_terms'}
    ranks = {'importance_score','scope_level','study_priority'}
    counts = {'degree','connected_edge_count'}
    ids, keys, lookup = set(), set(), {}
    for i,node in enumerate(result['nodes']):
        loc=f'/nodes/{i}'
        if not isinstance(node,dict): _fail('field_type',loc,'Expected node object')
        for spec in fields(GraphBundleNode):
            value=node.get(spec.name)
            if spec.name in node_lists:
                valid=isinstance(value,list) and all(isinstance(v,str) for v in value)
            elif spec.name in ranks: valid=type(value) is int and 1<=value<=5
            elif spec.name in counts: valid=type(value) is int and value>=0
            else: valid=isinstance(value,str) and (bool(value.strip()) if spec.name in {'node_id','concept_key','concept_name','metadata_path','metadata_url','concept_url'} else True)
            if not valid: _fail('field_type',loc+'/'+spec.name,'Invalid/missing node field')
        if node['node_id'] in ids: _fail('duplicate_id',loc+'/node_id','Duplicate node ID')
        if node['concept_key'] in keys: _fail('duplicate_key',loc+'/concept_key','Duplicate concept key')
        ids.add(node['node_id']);keys.add(node['concept_key']);lookup[node['node_id']]=node
        _validate_node_urls(node,paths,version,loc,check_files)
    degrees=Counter();relations=Counter()
    for i,edge in enumerate(result['edges']):
        loc=f'/edges/{i}'
        if not isinstance(edge,dict): _fail('field_type',loc,'Expected edge object')
        for spec in fields(GraphBundleEdge):
            value=edge.get(spec.name)
            if spec.name in {'supporting_courses','supporting_lecture_files'}: valid=isinstance(value,list) and all(isinstance(v,str) for v in value)
            elif spec.name=='supporting_lecture_hashes': valid=isinstance(value,dict) and all(isinstance(k,str) and isinstance(v,str) for k,v in value.items())
            elif spec.name=='target_resolved': valid=type(value) is bool
            else: valid=isinstance(value,str) and bool(value.strip())
            if not valid: _fail('field_type',loc+'/'+spec.name,'Invalid/missing edge field')
        if edge['edge_id'] in ids: _fail('duplicate_id',loc+'/edge_id','Duplicate graph ID')
        ids.add(edge['edge_id'])
        if edge['source'] not in lookup or edge['target'] not in lookup: _fail('dangling_endpoint',loc,'Missing edge endpoint')
        if edge['source']==edge['target']: _fail('self_edge',loc,'Self edge not supported')
        if any(edge[p+'_concept_key']!=lookup[edge[p]]['concept_key'] for p in ('source','target')): _fail('endpoint_key',loc,'Endpoint key mismatch')
        if not edge['target_resolved']: _fail('unresolved_edge',loc,'Unresolved edge')
        if edge['relation_type'] not in {'prerequisite','related'}: _fail('relation_type',loc,'Unsupported relation')
        degrees[edge['source']]+=1;degrees[edge['target']]+=1;relations[edge['relation_type']]+=1
    for i,node in enumerate(result['nodes']):
        if node['degree']!=degrees[node['node_id']] or node['connected_edge_count']!=degrees[node['node_id']]:
            _fail('node_degree',f'/nodes/{i}','Incident edge count mismatch')
    n,e=len(result['nodes']),len(result['edges'])
    expected={'total_concepts':n,'total_edges':e,'domains':sorted({v['domain'] for v in result['nodes'] if v['domain'].strip()}),
        'average_node_degree':((400*e+n)//(2*n))/100 if n else 0,
        'multi_course_concepts':sum(len(set(v['contributing_courses']))>1 for v in result['nodes']), 'relation_counts':dict(sorted(relations.items()))}
    stats=result.get('stats')
    if not isinstance(stats,dict):_fail('field_type','/stats','Expected stats object')
    for key,value in expected.items():
        actual=stats.get(key)
        if key in {'total_concepts','total_edges','multi_course_concepts'}: valid=type(actual) is int
        elif key=='average_node_degree': valid=type(actual) in {int,float} and math.isfinite(actual)
        elif key=='relation_counts': valid=isinstance(actual,dict) and all(type(v) is int for v in actual.values())
        else: valid=isinstance(actual,list) and all(isinstance(v,str) for v in actual)
        if not valid or actual!=value:_fail('stats','/stats/'+key,'Statistics mismatch')
    return result


def load_graph_bundle(path: Path, *, paths: GraphPresentationPaths, check_files: bool = False) -> dict:
    try:
        if path.is_symlink():_fail('unsafe_output',str(path),'Symlink graph bundle')
        payload=json.loads(path.read_bytes())
    except (OSError,ValueError) as exc:
        if isinstance(exc,GraphContractError):raise
        _fail('io_error',str(path),str(exc))
    return validate_graph_payload(payload,paths=paths,check_files=check_files)
