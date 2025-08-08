from dataclasses import dataclass

from app.application.dtos import MetadataDTO


@dataclass
class BoardCreateDTO:
    name: str
    position: int


@dataclass
class BoardUpdateDTO(BoardCreateDTO):
    ...


@dataclass
class BoardDTO(BoardCreateDTO, MetadataDTO):
    id: str
