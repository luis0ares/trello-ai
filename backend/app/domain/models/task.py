from dataclasses import dataclass
from datetime import datetime


@dataclass
class TaskCreateModel:
    board_id: int
    title: str
    description: str | None
    position: int


@dataclass
class TaskUpdateModel:
    board_id: int
    title: str
    description: str | None
    position: int


@dataclass
class TaskModel:
    id: int
    external_id: int
    board_id: int
    title: str
    description: str | None
    position: int
    created_at: datetime
    updated_at: datetime | None
