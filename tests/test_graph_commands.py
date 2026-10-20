import json
import shutil
import subprocess
import sys
from pathlib import Path
import pytest
from graph_fixtures import presentation_tree, FIXTURES

ROOT=Path(__file__).resolve().parents[1]

def command(script,*args):
    return subprocess.run([sys.executable,str(ROOT/script),*map(str,args)],cwd=ROOT,text=True,capture_output=True)

def inventory(root):
    return {str(p.relative_to(root)):(p.read_bytes(),p.stat().st_mtime_ns) for p in root.rglob('*') if p.is_file()}

def built(tmp_path):
    paths,_,_=presentation_tree(tmp_path)
    for root in (paths.concepts_root,paths.refined_root):
        p=root/'Linear Regression/metadata.json';data=json.loads(p.read_bytes());data['prerequisites']=['Probability'];p.write_text(json.dumps(data))
    graphs=tmp_path/'graphs'
    args=['--repo-root',tmp_path,'--graphs',graphs]
    result=command('scripts/build_graph.py',*args)
    return paths,graphs,args,result


def test_build_cli_exports_v2_and_noops(tmp_path):
    paths,graphs,args,result=built(tmp_path)
    assert result.returncode==0,result.stderr
    data=json.loads((graphs/'graph.json').read_bytes())
    assert data['schema_version']==2 and len(data['nodes'])==2 and len(data['edges'])==1
    before=inventory(graphs)
    second=command('scripts/build_graph.py',*args)
    assert second.returncode==0,second.stderr
    assert inventory(graphs)==before


def test_export_failure_preserves_presentation(tmp_path):
    paths,graphs,args,result=built(tmp_path)
    assert result.returncode==0,result.stderr
    p=paths.concepts_root/'Probability/metadata.json';data=json.loads(p.read_bytes());data['version_number']=2;p.write_text(json.dumps(data))
    published=graphs/'graph.json';before=(published.read_bytes(),published.stat().st_mtime_ns)
    failed=command('scripts/build_graph.py',*args)
    assert failed.returncode==1 and 'Traceback' not in failed.stderr
    assert json.loads(failed.stderr)['issues'][0]['code']=='node_metadata_mismatch'
    assert (published.read_bytes(),published.stat().st_mtime_ns)==before


@pytest.mark.parametrize('version',[1,2])
def test_presentation_check_requires_only_static_package(tmp_path,version):
    paths,_,_=presentation_tree(tmp_path)
    shutil.rmtree(paths.concepts_root)
    graphs=tmp_path/'graphs';graphs.mkdir()
    (graphs/'graph.json').write_bytes((FIXTURES/f'valid-v{version}.json').read_bytes())
    args=['--repo-root',tmp_path,'--graphs',graphs,'--presentation']
    before=inventory(tmp_path)
    checked=command('evaluation/evaluate_graph.py',*args)
    assert checked.returncode==0,checked.stderr
    assert json.loads(checked.stdout)==dict(valid=True,schema_version=version,node_count=2,edge_count=1)
    assert inventory(tmp_path)==before
    (paths.refined_root/'Probability/concept.md').unlink()
    failed=command('evaluation/evaluate_graph.py',*args)
    assert failed.returncode==1 and json.loads(failed.stderr)['issues']


def test_invalid_output_preflight_and_missing_bundle(tmp_path):
    paths,_,_=presentation_tree(tmp_path)
    before=inventory(tmp_path)
    failed=command('scripts/build_graph.py','--repo-root',tmp_path,'--graphs',paths.refined_root)
    assert failed.returncode==1 and json.loads(failed.stderr)['issues']
    assert inventory(tmp_path)==before
    checked=command('evaluation/evaluate_graph.py','--repo-root',tmp_path,'--graphs',tmp_path/'missing','--presentation')
    assert checked.returncode==1 and json.loads(checked.stderr)['issues'][0]['code']=='io_error'
    assert command('evaluation/evaluate_graph.py','--unknown').returncode==2
    metrics=command('evaluation/evaluate_graph.py','--graphs',tmp_path/'missing')
    assert metrics.returncode==0 and 'integrity_score' in json.loads(metrics.stdout)


def test_output_ancestor_symlink_cli_preflight_preserves_external_tree(tmp_path):
    repo = tmp_path/'repo'
    presentation_tree(repo)
    outside = tmp_path/'outside'
    outside.mkdir()
    (repo/'output-alias').symlink_to(outside, target_is_directory=True)
    failed = command('scripts/build_graph.py', '--repo-root', repo,
                     '--graphs', repo/'output-alias'/'nested')
    assert failed.returncode == 1, failed.stdout
    assert json.loads(failed.stderr)['issues'][0]['code'] == 'unsafe_output'
    assert list(outside.iterdir()) == []
