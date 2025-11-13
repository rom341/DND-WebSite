class CharacterPositionContextContainer:
    """Class to encapsulate character position context data"""
    def __init__(self, character_positions=None):
        self.character_positions = character_positions if character_positions is not None else []

    def get_context(self) -> dict:
        """Return context dictionary for character positions"""
        return self.__dict__.copy()