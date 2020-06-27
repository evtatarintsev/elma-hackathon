from typing import List
from xml.etree import ElementTree as ETree

from xml.dom import minidom

from .models import Type
from .services import get_type


def to_xsd(type: Type, ns: str = 'xs'):
    root = ETree.Element(f'{ns}:schema', attrib={f'xmlns:{ns}': 'http://www.w3.org/2001/XMLSchema'})
    return make_xsd(type, root, ns=ns)


def make_complex_types(
        root: ETree.Element,
        type: Type,
        ns: str,
        declared_types: List[str],
):
    type_el = ETree.Element(f'{ns}:complexType', attrib={'name': type.name})
    seq_el = ETree.Element(f'{ns}:sequence')

    root.append(type_el)
    type_el.append(seq_el)

    for el in type.elements or []:
        element = ETree.Element(f'{ns}:element', attrib={'name': el.name, 'type': el.type})
        seq_el.append(element)

        el_type = get_type(el.type)
        if not el_type.is_builtin and el.type not in declared_types:
            declared_types.append(el.type)
            make_complex_types(root, el_type, ns, declared_types)


def make_xsd(type: Type, root: ETree.Element, ns) -> str:
    declared_types = []

    for el in type.elements or []:
        element = ETree.Element(f'{ns}:element', attrib={'name': el.name, 'type': el.type})
        root.append(element)

        el_type = get_type(el.type)
        if not type.is_builtin and el.type not in declared_types:
            declared_types.append(el.type)
            make_complex_types(root, el_type, ns, declared_types)

    return minidom.parseString(ETree.tostring(root)).toprettyxml(indent="   ")
