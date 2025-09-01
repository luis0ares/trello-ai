from dataclasses import asdict
from logging import Logger

from app.application.dtos.board_dto import BoardCreateDTO, BoardDTO
from app.domain.models.board import BoardCreateModel
from app.domain.repositories.board_repository import BoardRepository


class CreateBoardUseCase:
    def __init__(self, logger: Logger, board_repository: BoardRepository):
        self.logger = logger
        self.board_repository = board_repository

    async def execute(self, board_data: BoardCreateDTO) -> BoardDTO:
        """
        Create a new board with the provided data.

        :param board_data: object containing the board details.
        :return: The created board object.
        """
        if not isinstance(board_data, BoardCreateDTO):
            raise ValueError("Invalid payload type")
        self.logger.debug(f"Creating board: {asdict(board_data)}")

        # Create the board using the repository
        to_create = BoardCreateModel(
            name=board_data.name,
            position=board_data.position,
        )

        created = await self.board_repository.create(to_create)
        self.logger.info(
            f"Board with external ID {created.external_id} created.")
        self.logger.debug(f"Created board: {asdict(created)}")

        return BoardDTO(
            id=str(created.external_id),
            name=created.name,
            position=created.position,
            created_at=created.created_at,
            updated_at=created.updated_at
        )
