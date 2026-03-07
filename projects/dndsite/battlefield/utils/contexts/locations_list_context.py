from dataclasses import asdict, dataclass
from typing import Optional

from django.db.models.query import QuerySet

from battlefield.models import Location


@dataclass
class LocationsListContext:
    locations_list: Optional[QuerySet[Location]]

    def to_dict(self) -> dict:
        return asdict(self)