from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ResourseNotFound
from app.domain.models.task import (
    TaskCreateModel,
    TaskModel,
    TaskUpdateModel,
)
from app.domain.repositories.task_repository import TaskRepository
from app.infrastructure.db.models import TaskEntity


class TaskRepositoryImpl(TaskRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, task_data: TaskCreateModel) -> TaskModel:
        if not isinstance(task_data, TaskCreateModel):
            raise ValueError("Invalid payload type")
        try:
            new_task = TaskEntity(
                board_id=task_data.board_id,
                title=task_data.title,
                description=task_data.description,
                position=task_data.position,
            )
            self.db_session.add(new_task)
            await self.db_session.commit()
            await self.db_session.refresh(new_task)

            return TaskModel(
                id=new_task.id,
                external_id=new_task.external_id,
                board_id=new_task.board_id,
                title=new_task.title,
                description=new_task.description,
                position=new_task.position,
                created_at=new_task.created_at,
                updated_at=new_task.updated_at
            )
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def get_all(self) -> List[TaskModel]:
        stmt = select(TaskEntity).order_by(TaskEntity.position)
        result = await self.db_session.execute(stmt)
        tasks = result.scalars().all()

        return [TaskModel(
            id=task.id,
            external_id=task.external_id,
            board_id=task.board_id,
            title=task.title,
            description=task.description,
            position=task.position,
            created_at=task.created_at,
            updated_at=task.updated_at
        ) for task in tasks]

    async def update(
            self, task_id: int, task_data: TaskUpdateModel) -> TaskModel:
        if not isinstance(task_data, TaskUpdateModel):
            raise ValueError("Invalid payload type")
        try:
            stmt = select(TaskEntity).where(TaskEntity.external_id == task_id)
            result = await self.db_session.execute(stmt)
            task_entity = result.scalar_one_or_none()

            if not task_entity:
                raise ResourseNotFound("Task not found")

            task_entity.board_id = task_data.board_id
            task_entity.title = task_data.title
            task_entity.description = task_data.description
            task_entity.position = task_data.position

            await self.db_session.commit()
            await self.db_session.refresh(task_entity)

            return TaskModel(
                id=task_entity.id,
                external_id=task_entity.external_id,
                board_id=task_entity.board_id,
                title=task_entity.title,
                description=task_entity.description,
                position=task_entity.position,
                created_at=task_entity.created_at,
                updated_at=task_entity.updated_at
            )
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def delete(self, task_id: int) -> bool:
        try:
            stmt = select(TaskEntity).where(
                TaskEntity.external_id == task_id)
            result = await self.db_session.execute(stmt)
            task_entity = result.scalar_one_or_none()

            if not task_entity:
                raise ResourseNotFound("Task not found")

            await self.db_session.delete(task_entity)
            await self.db_session.commit()
            return True
        except Exception as e:
            await self.db_session.rollback()
            raise e
