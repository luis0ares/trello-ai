from dataclasses import dataclass
from datetime import datetime


@dataclass
class BoardCreateModel:
    name: str
    position: int


@dataclass
class BoardUpdateModel:
    name: str
    position: int


@dataclass
class BoardModel:
    id: int
    external_id: int
    name: str
    position: int
    created_at: datetime
    updated_at: datetime | None
