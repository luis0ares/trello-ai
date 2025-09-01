from dataclasses import asdict
from logging import Logger

from app.application.dtos.board_dto import BoardDTO, BoardUpdateDTO
from app.domain.models.board import BoardUpdateModel
from app.domain.repositories.board_repository import BoardRepository


class UpdateBoardUseCase:
    def __init__(self, logger: Logger, board_repository: BoardRepository):
        self.logger = logger
        self.board_repository = board_repository

    async def execute(self, board_id: int,
                      board_data: BoardUpdateDTO) -> BoardDTO:
        """
        Update an existing board with the provided data.

        :param board_id: The external ID of the board to update.
        :param board_data: object containing the updated board details.
        :return: The updated board object.
        """
        if not isinstance(board_data, BoardUpdateDTO):
            raise ValueError("Invalid payload type")
        self.logger.debug(
            f"Updating board with external ID: {board_id} - {asdict(board_data)}")

        to_update = BoardUpdateModel(
            name=board_data.name,
            position=board_data.position,
        )

        updated = await self.board_repository.update(board_id, to_update)
        self.logger.info(
            f"Board with external ID {updated.external_id} updated.")
        self.logger.debug(f"Updated board: {asdict(updated)}")

        return BoardDTO(
            id=str(updated.external_id),
            name=updated.name,
            position=updated.position,
            created_at=updated.created_at,
            updated_at=updated.updated_at
        )
