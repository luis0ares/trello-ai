

from app.presentation.schemas import BaseSchema, MetaDataSchema


class BoardCreate(BaseSchema):
    name: str
    position: int = 0

class BoardUpdate(BoardCreate):
    ...

class BoardResponse(BoardCreate, MetaDataSchema):
    id: str