import json


def lecture_bytes(*, pages, course_id='C1', course_name='', pdf='C1/L1.pdf', page_count=None):
    return json.dumps({'course': {'course_id': course_id, 'course_name': course_name},
                      'pdf': pdf, 'page_count': len(pages) if page_count is None else page_count,
                      'pages': pages}, ensure_ascii=False).encode()


def example_pages():
    return [{'page_number': 1, 'heading': 'Regression',
             'extracted_text': '  Linear Regression is a statistical model relating inputs to a numeric response.\r\nnext',
             'concept_candidates': ['Linear Regression'],
             'concepts': [{'concept_name': 'Linear Regression', 'canonical_key': 'linear regression',
                           'importance_score': 5, 'evidence': '  x = 1; μ = 2  '}]}]
