from dataclasses import dataclass
from datetime import datetime
import json
from typing import List


BUILTINS = [
    'number',
    'decimal',
    'string',
    'boolean',
]


@dataclass
class Element:
    name: str
    type: str


@dataclass
class Type:
    name: str
    elements: List[Element] = None
    editable: bool = True
    version: int = 0
    updated: datetime = None

    @property
    def is_builtin(self):
        return self.name in BUILTINS

    def dump_elements(self) -> str:
        return json.dumps([{"name": el.name, "type": el.type} for el in self.elements])


@dataclass
class Diff:
    saved: List[Element]
    draft: List[Element]

    @property
    def is_empty(self) -> bool:
        return not self.saved and not self.draft
