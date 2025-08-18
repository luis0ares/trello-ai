from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.board import (
    BoardCreateModel,
    BoardModel,
    BoardUpdateModel,
    BoardWithTasksModel
)
from app.domain.models.task import TaskModel
from app.domain.repositories.board_repository import BoardRepository
from app.infrastructure.db.models import BoardEntity


class BoardRepositoryImpl(BoardRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, board_data: BoardCreateModel) -> BoardModel:
        if not isinstance(board_data, BoardCreateModel):
            raise ValueError("Invalid payload type")
        try:
            new_board = BoardEntity(
                name=board_data.name,
                position=board_data.position,
            )
            self.db_session.add(new_board)
            await self.db_session.commit()
            await self.db_session.refresh(new_board)

            return BoardModel(
                id=new_board.id,
                external_id=new_board.external_id,
                name=new_board.name,
                position=new_board.position,
                created_at=new_board.created_at,
                updated_at=new_board.updated_at
            )
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def get_all(self) -> List[BoardWithTasksModel]:
        stmt = select(BoardEntity).order_by(BoardEntity.position)
        result = await self.db_session.execute(stmt)
        boards = result.scalars().all()

        return [BoardWithTasksModel(
            id=board.id,
            external_id=board.external_id,
            name=board.name,
            position=board.position,
            created_at=board.created_at,
            updated_at=board.updated_at,
            tasks=[TaskModel(
                id=task.id,
                external_id=task.external_id,
                board_id=board.id,
                title=task.title,
                description=task.description,
                position=task.position,
                created_at=task.created_at,
                updated_at=task.updated_at
            ) for task in board.tasks]
        ) for board in boards]
    
    async def get_by_external_id(self, external_id: int) -> BoardModel | None:
        stmt = select(BoardEntity).where(
            BoardEntity.external_id == external_id)
        result = await self.db_session.execute(stmt)
        board_entity = result.scalar_one_or_none()

        if not board_entity:
            return None

        return BoardModel(
            id=board_entity.id,
            external_id=board_entity.external_id,
            name=board_entity.name,
            position=board_entity.position,
            created_at=board_entity.created_at,
            updated_at=board_entity.updated_at
        )

    async def update(
            self, board_id: int, board_data: BoardUpdateModel) -> BoardModel:
        if not isinstance(board_data, BoardUpdateModel):
            raise ValueError("Invalid payload type")
        try:
            stmt = select(BoardEntity).where(
                BoardEntity.external_id == board_id)
            result = await self.db_session.execute(stmt)
            board_entity = result.scalar_one_or_none()

            if not board_entity:
                raise ValueError("Board not found")

            board_entity.name = board_data.name
            board_entity.position = board_data.position

            await self.db_session.commit()
            await self.db_session.refresh(board_entity)

            return BoardModel(
                id=board_entity.id,
                external_id=board_entity.external_id,
                name=board_entity.name,
                position=board_entity.position,
                created_at=board_entity.created_at,
                updated_at=board_entity.updated_at
            )
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def delete(self, board_id: int) -> bool:
        try:
            stmt = select(BoardEntity).where(
                BoardEntity.external_id == board_id)
            result = await self.db_session.execute(stmt)
            board_entity = result.scalar_one_or_none()

            if not board_entity:
                raise ValueError("Board not found")

            await self.db_session.delete(board_entity)
            await self.db_session.commit()
            return True
        except Exception as e:
            await self.db_session.rollback()
            raise e
