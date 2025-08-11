from app.application.dtos.board_dto import BoardCreateDTO, BoardDTO
from app.domain.models.board import BoardCreateModel
from app.domain.repositories.board_repository import BoardRepository


class CreateBoardUseCase:
    def __init__(self, board_repository: BoardRepository):
        self.board_repository = board_repository

    async def execute(self, board_data: BoardCreateDTO) -> BoardDTO:
        """
        Create a new board with the provided data.

        :param board_data: object containing the board details.
        :return: The created board object.
        """
        if not isinstance(board_data, BoardCreateDTO):
            raise ValueError("Invalid payload type")

        # Create the board using the repository
        to_create = BoardCreateModel(
            name=board_data.name,
            position=board_data.position,
        )

        created_board = await self.board_repository.create(to_create)

        return BoardDTO(
            id=str(created_board.external_id),
            name=created_board.name,
            position=created_board.position,
            created_at=created_board.created_at,
            updated_at=created_board.updated_at
        )
