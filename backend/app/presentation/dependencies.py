from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.database import get_session
from app.infrastructure.db.impl.board_repository_impl import (
    BoardRepositoryImpl)
from app.infrastructure.db.impl.task_repository_impl import (
    TaskRepositoryImpl)

_DbSession = Annotated[AsyncSession, Depends(get_session)]


def get_board_repository(session: _DbSession) -> BoardRepositoryImpl:
    return BoardRepositoryImpl(db_session=session)


def get_task_repository(session: _DbSession) -> TaskRepositoryImpl:
    return TaskRepositoryImpl(db_session=session)


BoardRepository = Annotated[BoardRepositoryImpl, Depends(get_board_repository)]
TaskRepository = Annotated[BoardRepositoryImpl, Depends(get_task_repository)]
