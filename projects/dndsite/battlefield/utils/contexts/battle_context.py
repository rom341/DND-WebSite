class BattlefieldContextContainer:
    """Class to encapsulate battle context data"""
    def __init__(self, group_id, rows_count=10, cols_count=10, characters=None, 
                 move_character_form=None, add_character_form=None, add_user_form=None):
        self.group_id = group_id
        self.rows_count = rows_count
        self.cols_count = cols_count
        self.rows_range = range(rows_count)
        self.cols_range = range(cols_count)
        self.characters = characters if characters is not None else []
        self.move_character_form = move_character_form
        self.add_character_form = add_character_form
        self.add_user_form = add_user_form


    def get_context(self) -> dict:
        """Return context dictionary for battle rendering"""
        return self.__dict__