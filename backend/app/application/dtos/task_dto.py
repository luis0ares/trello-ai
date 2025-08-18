from dataclasses import dataclass
from datetime import datetime


@dataclass
class TaskCreateDTO:
    board_id: int
    title: str
    description: str | None
    position: int


@dataclass
class TaskUpdateDTO:
    board_id: int
    title: str
    description: str | None
    position: int


@dataclass
class TaskDTO:
    id: str
    board_id: str
    title: str
    description: str | None
    position: int
    created_at: datetime | None
    updated_at: datetime | None
