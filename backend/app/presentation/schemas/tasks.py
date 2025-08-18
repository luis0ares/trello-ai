from app.presentation.schemas import BaseSchema, MetaDataSchema


class TaskCreate(BaseSchema):
    board_id: str
    title: str
    description: str | None = None
    position: int = 0


class TaskUpdate(TaskCreate):
    ...


class TaskResponse(TaskCreate, MetaDataSchema):
    id: str
    board_id: str
