
from dataclasses import asdict, dataclass, field
from typing import Optional

from django.db.models.query import QuerySet

from battlefield.models import CharacterPosition, Location


@dataclass
class LocationMapContext:
    current_location: Optional[Location]
    rows_count: int
    cols_count: int
    character_positions: Optional[QuerySet[CharacterPosition]]
    
    rows_range: range = field(init=False)
    cols_range: range = field(init=False)

    def __post_init__(self):
        self.rows_range = range(self.rows_count)
        self.cols_range = range(self.cols_count)

    def to_dict(self):
        return asdict(self)
