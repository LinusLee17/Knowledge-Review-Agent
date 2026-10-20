from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
import json

from knowledge_review_agent.graph_bundle import GraphPresentationPaths
from knowledge_review_agent.models import ConceptMetadata, GraphNode, GraphEdge

STAMP = '2026-10-20T00:00:00+00:00'
FIXTURES = Path(__file__).parent / 'fixtures' / 'graph_presentation'


def apply_case(payload, operations):
    result = deepcopy(payload)
    for op in operations:
        target = result
        for key in op['path'][:-1]: target = target[key]
        if op['op'] == 'remove': del target[op['path'][-1]]
        else: target[op['path'][-1]] = deepcopy(op['value'])
    return result


def presentation_tree(tmp_path):
    paths = GraphPresentationPaths(tmp_path, tmp_path/'knowledge_base/concepts', tmp_path/'knowledge_base/refined', tmp_path/'website')
    paths.website_root.mkdir(parents=True)
    (paths.website_root/'concept.html').write_text('<html>Concept viewer</html>')
    nodes=[]
    for name, key, identifier in [('Probability','probability','p'), ('Linear Regression','linear regression','r')]:
        metadata=ConceptMetadata(concept_name=name, canonical_key=key, domain='Statistics', topic='Models',
            importance_score=3, contributing_courses=['C1'], contributing_lecture_files=['C1/L1/lecture.json'],
            last_updated_timestamp=STAMP, definition=name+' is an exact published definition.', graph_node_id=identifier)
        for root in (paths.concepts_root, paths.refined_root):
            directory=root/name
            directory.mkdir(parents=True)
            (directory/'metadata.json').write_text(json.dumps(asdict(metadata)))
            (directory/'concept.md').write_text(f'# {name}\n\n## Definition\n{metadata.definition}\n\n## Core Intuition\nExact published intuition.\n')
        nodes.append(GraphNode(identifier,key,name,str(paths.concepts_root/name/'metadata.json'),1,STAMP,
            domain='Statistics',topic='Models',importance_score=3,scope_level=metadata.scope_level,
            study_priority=3,contributing_courses=['C1'],contributing_lecture_files=['C1/L1/lecture.json'],graph_node_id=identifier))
    edge=GraphEdge('e','p','probability','r','linear regression','prerequisite',True,
        'Probability','Linear Regression',supporting_courses=['C1'],supporting_lecture_files=['C1/L1/lecture.json'])
    return paths,nodes,[edge]
