from dataclasses import dataclass
from datetime import datetime


@dataclass
class MetadataDTO:
    created_at: datetime
    updated_at: datetime
