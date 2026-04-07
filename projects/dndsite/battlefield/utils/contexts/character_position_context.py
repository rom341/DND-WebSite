from dataclasses import asdict, dataclass
from typing import Optional

from django.db.models.query import QuerySet

from location.models import CharacterPosition


@dataclass
class CharacterPositionContextContainer:
    character_positions: Optional[QuerySet[CharacterPosition]]

    def to_dict(self) -> dict:
        return asdict(self)
    
    def get_context(self):
        return self.to_dict()
