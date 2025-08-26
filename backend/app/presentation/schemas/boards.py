from typing import List

from app.presentation.schemas import BaseSchema, MetaDataSchema
from app.presentation.schemas.tasks import TaskResponse


class BoardCreate(BaseSchema):
    name: str
    position: int = 0


class BoardUpdate(BoardCreate):
    ...


class BoardResponse(BoardCreate, MetaDataSchema):
    id: str
    tasks: List[TaskResponse] = []
