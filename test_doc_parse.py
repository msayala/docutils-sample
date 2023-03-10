import docutils
import pytest

import doc_parse
from doc_parse import Field


MULTILINE_DOCSTRING = """
Full sentence of text describing this code.

Note:
Literally any other non-parameter text.

:ivar num: A number value
:ivar bool_param: a bool param
:ivar long_doc: This is intended to be a multiline param
    description so that we can test line breaks.
:customtag foo: A custom tag that we make up and parse how we want
"""


def test_parse_field():
    docstring = """:param foo: my description"""
    document = doc_parse.make_document(docstring)
    raw_fields = list(document.findall(docutils.nodes.field))
    # sanity check
    assert len(raw_fields) == 1
    assert doc_parse.parse_field(raw_fields[0]) == Field(
        tag='param', name='foo', description='my description')


def test_parse_fields_integration():
    document = doc_parse.make_document(MULTILINE_DOCSTRING)
    raw_fields = document.findall(docutils.nodes.field)
    parsed_fields = [doc_parse.parse_field(raw_field) for raw_field in
                     raw_fields]
    assert parsed_fields == [
        Field(tag='ivar', name='num', description='A number value'),
        Field(tag='ivar', name='bool_param', description='a bool param'),
        Field(tag='ivar', name='long_doc', description=(
            'This is intended to be a multiline param description so that we '
            'can test line breaks.')),
        Field(tag='customtag', name='foo', description=(
            'A custom tag that we make up and parse how we want'))
    ], parsed_fields