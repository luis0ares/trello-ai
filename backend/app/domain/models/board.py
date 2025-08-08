from dataclasses import dataclass

from app.domain.models import MetadataModel


@dataclass
class BoardModel(MetadataModel):
    id: int
    external_id: str
    name: str
    position: int
