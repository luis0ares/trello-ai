from dataclasses import dataclass
from datetime import datetime


@dataclass
class BoardCreateDTO:
    name: str
    position: int


@dataclass
class BoardUpdateDTO:
    name: str
    position: int


@dataclass
class BoardDTO:
    id: str
    name: str
    position: int
    created_at: datetime | None
    updated_at: datetime | None
