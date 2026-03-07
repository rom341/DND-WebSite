from dataclasses import asdict, dataclass
from typing import Optional

from django.db.models.query import QuerySet


@dataclass
class LocationsListContext:
    locations_list: Optional[QuerySet]


    def to_dict(self) -> dict:
        return asdict(self)