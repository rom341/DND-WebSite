
from dataclasses import asdict, dataclass, field
from typing import Optional

from django.db.models.query import QuerySet

from characters.models import CharacterPosition
from location.models import Location
from django.forms.models import model_to_dict


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
        result = asdict(self)
        return result
    
    def to_dict_full(self):
        result = asdict(self)
        result["current_location"] = model_to_dict(self.current_location)
        result["character_positions"] = [model_to_dict(pos) for pos in self.character_positions]
        result['cols_range'] = list(self.cols_range)
        result['rows_range'] = list(self.rows_range)
        return result
