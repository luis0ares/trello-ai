from dataclasses import dataclass
from datetime import datetime
from typing import List

from app.config.tasks_prompt import StructuredReply


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


@dataclass
class TaskSuggestionDTO:
    final: bool
    message: str | None
    tasks: List[StructuredReply] | None
