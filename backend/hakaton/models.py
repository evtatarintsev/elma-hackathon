from dataclasses import dataclass
from datetime import datetime
from typing import List


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
