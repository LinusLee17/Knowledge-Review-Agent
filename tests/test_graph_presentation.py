import json
from copy import deepcopy
import pytest
from graph_fixtures import FIXTURES, apply_case, presentation_tree
from knowledge_review_agent.graph_bundle import validate_graph_payload, load_graph_bundle, GraphContractError


@pytest.mark.parametrize('filename',['valid-v2.json','valid-v1.json','empty-v2.json'])
def test_complete_contracts(tmp_path,filename):
    paths,_,_=presentation_tree(tmp_path)
    payload=json.loads((FIXTURES/filename).read_text())
    before=deepcopy(payload)
    result=validate_graph_payload(payload,paths=paths,check_files=True)
    assert payload==before and result['schema_version']==payload['schema_version']
    assert all('/refined/' in n['metadata_path'] for n in result['nodes'])


@pytest.mark.parametrize('case',json.loads((FIXTURES/'cases.json').read_text()),ids=lambda c:c['name'])
def test_contract_fixture_cases(tmp_path,case):
    paths,_,_=presentation_tree(tmp_path)
    payload=apply_case(json.loads((FIXTURES/case['base']).read_text()),case['operations'])
    before=deepcopy(payload)
    with pytest.raises(GraphContractError) as caught: validate_graph_payload(payload,paths=paths)
    assert caught.value.issues[0].code==case['code']
    assert caught.value.issues[0].location and payload==before


def test_stats_rounding_and_unicode_domains(tmp_path):
    paths,_,_=presentation_tree(tmp_path)
    payload=json.loads((FIXTURES/'empty-v2.json').read_text())
    template=json.loads((FIXTURES/'valid-v2.json').read_text())['nodes'][0]
    payload['nodes']=[{**template,'node_id':f'n{i}','concept_key':f'key{i}','degree':0,'connected_edge_count':0,
        'domain':'\ue000' if i==0 else '\U00010000'} for i in range(400)]
    edge=json.loads((FIXTURES/'valid-v2.json').read_text())['edges'][0]
    payload['edges']=[{**edge,'edge_id':f'e{i}','source':f'n{i}','target':f'n{i+1}',
        'source_concept_key':f'key{i}','target_concept_key':f'key{i+1}'} for i in range(9)]
    for e in payload['edges']:
        for endpoint in ('source','target'):
            n=payload['nodes'][int(e[endpoint][1:])];n['degree']+=1;n['connected_edge_count']+=1
    payload['stats'].update(total_concepts=400,total_edges=9,domains=['\ue000','\U00010000'],average_node_degree=.05,relation_counts={'prerequisite':9})
    assert validate_graph_payload(payload,paths=paths)['stats']['average_node_degree']==.05
    payload['stats']['average_node_degree']=.04
    with pytest.raises(GraphContractError): validate_graph_payload(payload,paths=paths)


def test_bundle_loader_rejects_bad_json(tmp_path):
    paths,_,_=presentation_tree(tmp_path)
    for raw in (None,'not JSON'):
        path=tmp_path/'bad.json'
        if raw is not None:path.write_text(raw)
        with pytest.raises(GraphContractError):load_graph_bundle(path,paths=paths)


@pytest.mark.parametrize('value',[float('nan'),float('inf'),True])
def test_numeric_values_are_strict(tmp_path,value):
    paths,_,_=presentation_tree(tmp_path)
    payload=json.loads((FIXTURES/'valid-v2.json').read_text())
    payload['stats']['average_node_degree']=value
    with pytest.raises(GraphContractError):validate_graph_payload(payload,paths=paths)


def test_export_uses_refined_snapshot_only(tmp_path,monkeypatch):
    from knowledge_review_agent.graph_bundle import build_graph_bundle
    paths,nodes,edges=presentation_tree(tmp_path)
    draft=paths.concepts_root/'Probability'/'metadata.json'
    draft.write_text('invalid draft must not be read')
    reads=[];read=type(draft).read_bytes
    def counted(p):
        assert not p.is_relative_to(paths.concepts_root)
        reads.append(p)
        return read(p)
    monkeypatch.setattr(type(draft),'read_bytes',counted)
    result=build_graph_bundle(nodes,edges,tmp_path/'output','2026-10-20T00:00:00Z',paths=paths)
    assert result.schema_version==2
    assert result.nodes[0].definition=='Probability is an exact published definition.'
    assert len(reads)==4 and len(set(reads))==4


def test_shared_markdown_sections_preserve_content(tmp_path):
    from knowledge_review_agent.graph_bundle import build_graph_bundle
    paths,nodes,edges=presentation_tree(tmp_path)
    md=paths.refined_root/'Probability'/'concept.md'
    md.write_text('# Probability\n## Core Intuition\nfirst\n```md\n## Interview Questions\nnot questions\n```\n## Core Intuition\nsecond\n')
    result=build_graph_bundle(nodes,edges,tmp_path/'out','2026-10-20T00:00:00Z',paths=paths)
    node=next(n for n in result.nodes if n.node_id=='p')
    assert 'first' in node.core_idea and 'second' in node.core_idea
    assert node.interview_notes=='' and '## Interview Questions' in node.core_idea


@pytest.mark.parametrize('damage',['missing','identity','version','domain','rank','courses','symlink'])
def test_invalid_last_node_preserves_existing_bundle(tmp_path,damage):
    from knowledge_review_agent.graph_bundle import write_graph_bundle
    paths,nodes,edges=presentation_tree(tmp_path)
    graphs=tmp_path/'graphs';graphs.mkdir()
    old=graphs/'graph.json';old.write_bytes(b'previous complete bundle')
    before=(old.read_bytes(),old.stat().st_mtime_ns)
    directory=paths.refined_root/'Linear Regression'
    path=directory/'metadata.json'
    data=json.loads(path.read_bytes())
    if damage=='missing':path.unlink()
    elif damage=='symlink':
        path.rename(tmp_path/'outside.json');path.symlink_to(tmp_path/'outside.json')
    else:
        field={'identity':'canonical_key','version':'version_number','domain':'domain','rank':'importance_score','courses':'contributing_courses'}[damage]
        data[field]={'identity':'other','version':9,'domain':'Other','rank':1,'courses':['Other']}[damage]
        path.write_text(json.dumps(data))
    with pytest.raises(GraphContractError):write_graph_bundle(graphs,nodes,edges,'2026-10-20T00:00:00Z',paths=paths)
    assert (old.read_bytes(),old.stat().st_mtime_ns)==before


def test_export_noop_and_atomic_update(tmp_path,monkeypatch):
    from knowledge_review_agent.graph_bundle import write_graph_bundle
    from dataclasses import replace
    import os
    paths,nodes,edges=presentation_tree(tmp_path)
    graphs=tmp_path/'graphs'
    path=write_graph_bundle(graphs,nodes,edges,'2026-10-20T00:00:00Z',paths=paths)
    before=(path.read_bytes(),path.stat().st_mtime_ns)
    write_graph_bundle(graphs,list(reversed(nodes)),edges,'2026-10-21T00:00:00Z',paths=paths)
    assert (path.read_bytes(),path.stat().st_mtime_ns)==before
    md=paths.refined_root/'Probability'/'metadata.json'
    payload=json.loads(md.read_bytes());payload['definition']='Changed exact definition.';md.write_text(json.dumps(payload))
    real=os.replace
    def fail(src,dst):raise OSError('simulated replace failure')
    with monkeypatch.context() as p:
        p.setattr(os,'replace',fail)
        with pytest.raises(GraphContractError):write_graph_bundle(graphs,nodes,edges,'2026-10-21T00:00:00Z',paths=paths)
    assert (path.read_bytes(),path.stat().st_mtime_ns)==before
    assert list(graphs.iterdir())==[path]
    write_graph_bundle(graphs,nodes,edges,'2026-10-21T00:00:00Z',paths=paths)
    assert json.loads(path.read_bytes())['generated_at']=='2026-10-21T00:00:00Z'


def test_custom_roots_and_url_roundtrip(tmp_path):
    from knowledge_review_agent.graph_bundle import build_graph_bundle, GraphPresentationPaths
    from dataclasses import replace
    from urllib.parse import urlsplit, parse_qs, unquote
    paths,nodes,edges=presentation_tree(tmp_path)
    name='A # & ? % μ/metadata.json examples'
    for root in (paths.concepts_root,paths.refined_root):
        target=root/name;target.parent.mkdir(parents=True)
        (root/'Probability').rename(target)
    nodes[0]=replace(nodes[0],metadata_path=str(paths.concepts_root/name/'metadata.json'))
    refined=tmp_path/'published/courses';refined.parent.mkdir()
    paths.refined_root.rename(refined)
    website=tmp_path/'site/ui';website.parent.mkdir()
    paths.website_root.rename(website)
    paths=replace(paths,refined_root=refined,website_root=website)
    bundle=build_graph_bundle(nodes,edges,tmp_path/'totally/different/output','2026-10-20T00:00:00Z',paths=paths)
    node=bundle.nodes[0]
    assert (website/unquote(node.metadata_url)).resolve()==(refined/name/'metadata.json').resolve()
    target=parse_qs(urlsplit(node.concept_url).query)['path'][0]
    assert (website/unquote(target)).resolve()==(refined/name/'concept.md').resolve()
    assert '/refined/Probability/' not in node.metadata_url
    assert node.metadata_path=='published/courses/'+name+'/metadata.json'


@pytest.mark.parametrize('damage',['root_symlink','file_symlink','overlap','absent_record'])
def test_output_and_absent_publication_protection(tmp_path,damage):
    from knowledge_review_agent.graph_bundle import write_graph_bundle
    paths,nodes,edges=presentation_tree(tmp_path)
    output=tmp_path/'graphs'
    if damage=='root_symlink':output.symlink_to(paths.refined_root,target_is_directory=True)
    elif damage=='file_symlink':
        output.mkdir();(output/'graph.json').symlink_to(paths.refined_root/'Probability/metadata.json')
    elif damage=='overlap':output=paths.refined_root/'graphs'
    else:(paths.refined_root/'Linear Regression/metadata.json').unlink()
    before={str(p):p.read_bytes() for p in paths.refined_root.rglob('*') if p.is_file()}
    with pytest.raises(GraphContractError):write_graph_bundle(output,nodes,edges,'2026-10-20T00:00:00Z',paths=paths)
    assert {str(p):p.read_bytes() for p in paths.refined_root.rglob('*') if p.is_file()}==before
    if damage=='absent_record':assert not output.exists()


def test_python_export_consumed_by_browser_contract(tmp_path):
    import subprocess
    from pathlib import Path
    from knowledge_review_agent.graph_bundle import write_graph_bundle
    paths,nodes,edges=presentation_tree(tmp_path)
    bundle=write_graph_bundle(tmp_path/'knowledge_base/graphs',nodes,edges,'2026-10-20T00:00:00Z',paths=paths)
    module=(Path(__file__).resolve().parents[1]/'website/graph-contract.mjs').as_uri()
    code="""import {readFile} from 'node:fs/promises';
const {validateGraphPayload}=await import(process.argv[1]);
const graph=validateGraphPayload(JSON.parse(await readFile(process.argv[2],'utf8')),{baseUrl:'http://example.test/website/index.html'});
console.log(JSON.stringify({nodes:graph.nodes.length,edges:graph.edges.length}));"""
    run=subprocess.run(['node','--input-type=module','-e',code,module,str(bundle)],capture_output=True,text=True)
    assert run.returncode==0,run.stderr
    assert json.loads(run.stdout)==dict(nodes=2,edges=1)


def test_output_ancestor_symlink_rejected_before_publication(tmp_path):
    from knowledge_review_agent.graph_bundle import write_graph_bundle, validate_graph_paths
    repo = tmp_path/'repo'
    paths, nodes, edges = presentation_tree(repo)
    outside = tmp_path/'outside'
    outside.mkdir()
    (repo/'output-alias').symlink_to(outside, target_is_directory=True)
    output = repo/'output-alias'/'nested'
    with pytest.raises(GraphContractError, match='Symlink'):
        validate_graph_paths(paths, graphs_root=output)
    with pytest.raises(GraphContractError):
        write_graph_bundle(output, nodes, edges, '2026-10-20T00:00:00Z', paths=paths)
    assert list(outside.iterdir()) == []


@pytest.mark.parametrize('existing_mode', [None, 0o640])
def test_publication_keeps_readable_file_permissions(tmp_path, existing_mode):
    from knowledge_review_agent.graph_bundle import write_graph_bundle
    from stat import S_IMODE
    paths, nodes, edges = presentation_tree(tmp_path)
    graphs = tmp_path/'graphs'
    if existing_mode is not None:
        graphs.mkdir()
        target = graphs/'graph.json'
        target.write_text('{}')
        target.chmod(existing_mode)
    published = write_graph_bundle(graphs, nodes, edges, '2026-10-20T00:00:00Z', paths=paths)
    assert S_IMODE(published.stat().st_mode) == (existing_mode if existing_mode is not None else 0o644)


def test_packaged_schema_one_readonly_compatibility():
    from pathlib import Path
    from knowledge_review_agent.graph_bundle import GraphPresentationPaths
    root=Path(__file__).resolve().parents[1]
    file=root/'knowledge_base/graphs/graph.json'
    before=(file.read_bytes(),file.stat().st_mtime_ns)
    paths=GraphPresentationPaths(root,root/'knowledge_base/concepts',root/'knowledge_base/refined',root/'website')
    result=load_graph_bundle(file,paths=paths,check_files=True)
    assert len(result['nodes'])==result['stats']['total_concepts']
    assert (file.read_bytes(),file.stat().st_mtime_ns)==before
