from dataclasses import dataclass
from datetime import datetime


@dataclass
class MetadataModel:
    created_at: datetime
    updated_at: datetime