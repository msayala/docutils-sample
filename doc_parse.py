import argparse
import typing
from docutils import frontend
from docutils import nodes
from docutils import utils
from docutils.parsers import rst


class Field(typing.NamedTuple):
    tag: str
    name: str
    description: str


def make_document(docstring: str) -> nodes.document:
    """
    Parse the supplied docstring and turn it into a "document", which is the
    parent node of a tree containing all elements of the docstring.
    """
    parser = rst.Parser()
    settings = frontend.get_default_settings(rst.Parser)
    # source_path doesn't matter since we don't write
    document = utils.new_document(source_path='foo', settings=settings)
    parser.parse(docstring, document)
    return document


def parse_field(raw_field: nodes.field) -> Field:
    """
    Parse a field node to extract the tag, name, and description of the given
    field.
    """
    field_name_idx = raw_field.first_child_matching_class(nodes.field_name)
    field_body_idx = raw_field.first_child_matching_class(nodes.field_body)
    if not all((field_name_idx is not None, field_body_idx is not None)):
        raise ValueError(f'Expected field {raw_field} to have both field_name '
                         f'and field_body.')
    field_name = raw_field.children[field_name_idx]
    tag, name = field_name.astext().split()
    field_body = raw_field.children[field_body_idx]
    description = field_body.astext().replace('\n', ' ')
    return Field(tag=tag, name=name, description=description)
