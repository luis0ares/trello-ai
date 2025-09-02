from logging import Logger
from typing import List

from app.application.dtos.board_dto import BoardWithTasksDTO
from app.application.dtos.task_dto import TaskDTO
from app.domain.repositories.board_repository import BoardRepository


class GetBoardsUseCase:
    def __init__(self, logger: Logger, board_repository: BoardRepository):
        self.logger = logger
        self.board_repository = board_repository

    async def execute(self) -> List[BoardWithTasksDTO]:
        """
        Retrieves all boards.

        :return: A list of boards.
        """
        boards = await self.board_repository.get_all()
        self.logger.debug(f"Retrieved {len(boards)} boards")

        return [BoardWithTasksDTO(
            id=str(board.external_id),
            name=board.name,
            position=board.position,
            created_at=board.created_at,
            updated_at=board.updated_at,
            tasks=[TaskDTO(
                id=str(task.external_id),
                board_id=str(board.external_id),
                title=task.title,
                description=task.description,
                position=task.position,
                created_at=task.created_at,
                updated_at=task.updated_at
            ) for task in board.tasks]
        ) for board in boards]
