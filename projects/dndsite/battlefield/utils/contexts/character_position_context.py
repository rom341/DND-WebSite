from dataclasses import asdict, dataclass
from typing import Optional

from django.db.models.query import QuerySet

from battlefield.models import CharacterPosition


@dataclass
class CharacterPositionContextContainer:
    character_positions: Optional[QuerySet[CharacterPosition]]

    def to_dict(self) -> dict:
        return asdict(self)
    
    def get_context(self):
        return self.to_dict()

# class CharacterPositionContextContainer:
#     """Class to encapsulate character position context data"""
#     def __init__(self, character_positions=None):
#         self.character_positions = character_positions if character_positions is not None else []

#     def get_context(self) -> dict:
#         """Return context dictionary for character positions"""
#         #return self.__dict__.copy()
#         positions_list = []
#         for p in self.character_positions:
#             positions_list.append({
#                 "id": p.character.id,
#                 "name": p.character.character_name,
#                 "row": p.row,
#                 "col": p.column,
#             })
        
#         return {
#             "character_positions": self.character_positions, 
#             "character_positions_dict": positions_list         
#         }