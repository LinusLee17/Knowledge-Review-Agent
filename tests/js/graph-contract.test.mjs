import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, mkdtemp, mkdir, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import http from 'node:http';
import { validateGraphPayload, loadGraphData, resolveConceptPath, GraphContractError } from '../../website/graph-contract.mjs';

const fixtures = new URL('../fixtures/graph_presentation/', import.meta.url);
const read = async name => JSON.parse(await readFile(new URL(name, fixtures), 'utf8'));
const options = {baseUrl:'https://example.test/website/index.html'};
function applyCase(payload, operations) {
  const result=structuredClone(payload);
  for(const op of operations) {
    let target=result;
    for(const key of op.path.slice(0,-1)) target=target[key];
    if(op.op==='remove') delete target[op.path.at(-1)];
    else target[op.path.at(-1)]=structuredClone(op.value);
  }
  return result;
}
for(const filename of ['valid-v2.json','valid-v1.json','empty-v2.json']) {
  test(`complete ${filename}`,async()=>{
    const data=await read(filename), before=structuredClone(data);
    const result=validateGraphPayload(data,options);
    assert.deepEqual(data,before);
    assert.equal(result.schema_version,data.schema_version);
    assert.ok(result.nodes.every(n=>n.metadata_path.includes('/refined/')));
  });
}
for(const c of await read('cases.json')) {
  test(`contract ${c.name}`,async()=>{
    const data=applyCase(await read(c.base),c.operations),before=structuredClone(data);
    assert.throws(()=>validateGraphPayload(data,options),e=>e instanceof GraphContractError && e.issues[0].code===c.code);
    assert.deepEqual(data,before);
  });
}
test('calendar, nonfinite and half-up tie',async()=>{
  const graph=await read('valid-v2.json');
  for(const bad of [NaN,Infinity,true]) {
    const data=structuredClone(graph); data.stats.average_node_degree=bad;
    assert.throws(()=>validateGraphPayload(data,options));
  }
  const data=await read('empty-v2.json');
  data.nodes=Array.from({length:400},(_,i)=>({...structuredClone(graph.nodes[0]),node_id:`n${i}`,concept_key:`key${i}`,degree:0,connected_edge_count:0,domain:i===0?'\ue000':'\u{10000}'}));
  data.edges=Array.from({length:9},(_,i)=>({...graph.edges[0],edge_id:`e${i}`,source:`n${i}`,target:`n${i+1}`,source_concept_key:`key${i}`,target_concept_key:`key${i+1}`}));
  for(const e of data.edges)for(const p of [e.source,e.target]) {const n=data.nodes[Number(p.slice(1))];n.degree++;n.connected_edge_count++;}
  Object.assign(data.stats,{total_concepts:400,total_edges:9,domains:['\ue000','\u{10000}'],average_node_degree:.05,relation_counts:{prerequisite:9}});
  assert.equal(validateGraphPayload(data,options).stats.average_node_degree,.05);
  data.stats.average_node_degree=.04;assert.throws(()=>validateGraphPayload(data,options));
});
test('loader fetches exactly graph bundle; no fallback',async()=>{
  const graph=await read('valid-v2.json'),calls=[];
  const result=await loadGraphData(options,async url=>{calls.push(String(url));return {ok:true,json:async()=>graph};});
  assert.equal(result.nodes.length,2);
  assert.deepEqual(calls,['https://example.test/knowledge_base/graphs/graph.json']);
  for(const response of [{ok:false,status:404},{ok:true,json:async()=>{throw new SyntaxError('bad JSON');}},{ok:true,json:async()=>({...graph,schema_version:9})}]) {
    const failures=[];
    await assert.rejects(loadGraphData(options,async url=>{failures.push(String(url));return response;}),GraphContractError);
    assert.equal(failures.length,1);
  }
  await assert.rejects(loadGraphData(options,async()=>{throw new Error('offline');}),GraphContractError);
});
test('published path guard',()=>{
  for(const raw of ['https://evil.test/concept.md','//evil.test/concept.md','/etc/concept.md',
    '../knowledge_base/refined-other/A/concept.md','../knowledge_base/refined/%2e%2e/private/concept.md',
    '../knowledge_base/refined/A%2f..%2fprivate/concept.md','../knowledge_base/refined/%zz/concept.md',
    '../knowledge_base/refined/A/metadata.json']) assert.throws(()=>resolveConceptPath(raw,options));
});
test('special filename and literal percent escape HTTP roundtrip',async()=>{
  const root=await mkdtemp(path.join(tmpdir(),'graph-contract-'));
  const server=http.createServer(async(req,res)=>{
    try{res.end(await readFile(path.join(root,decodeURIComponent(new URL(req.url,'http://local').pathname))));}
    catch{res.statusCode=404;res.end('missing');}
  });
  try {
    const name='A # & ? % μ %2F';
    const directory=path.join(root,'published',name);
    await mkdir(directory,{recursive:true});
    await writeFile(path.join(directory,'concept.md'),'# Exact special text');
    await writeFile(path.join(directory,'metadata.json'),'{}');
    await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
    const base=`http://127.0.0.1:${server.address().port}/site/ui/index.html`;
    const o={baseUrl:base,repoRootUrl:'../../',refinedRootUrl:'../../published/'};
    const data=await read('valid-v2.json');
    for(const n of data.nodes) {
      n.metadata_path=`published/${name}/metadata.json`;
      n.metadata_url=`../../published/${encodeURIComponent(name)}/metadata.json`;
      n.concept_url=`./concept.html?path=${encodeURIComponent(`../../published/${encodeURIComponent(name)}/concept.md`)}`;
    }
    const graph=validateGraphPayload(data,o);
    const viewer=new URL(graph.nodes[0].concept_url,base);
    const url=resolveConceptPath(viewer.searchParams.get('path'),o);
    assert.equal(await (await fetch(url)).text(),'# Exact special text');
    assert.equal(await (await fetch(new URL(graph.nodes[0].metadata_url,base))).text(),'{}');
  } finally {await new Promise(resolve=>server.close(resolve));await rm(root,{recursive:true,force:true});}
});

test('existing packaged bundle remains compatible without reconstruction',async()=>{
  const file=new URL('../../knowledge_base/graphs/graph.json',import.meta.url);
  const raw=await readFile(file,'utf8');
  const graph=validateGraphPayload(JSON.parse(raw),options);
  assert.equal(graph.nodes.length,graph.stats.total_concepts);
  assert.equal(await readFile(file,'utf8'),raw);
});
