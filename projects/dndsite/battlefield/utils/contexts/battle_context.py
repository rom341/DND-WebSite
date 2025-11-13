class BattlefieldContextContainer:
    """Class to encapsulate battle context data"""
    def __init__(self, current_group_id, current_group=None,
                 locations_list=None,
                 move_character_form=None, add_character_form=None, add_user_form=None, create_location_form=None,
                 location_map_context=None
                 ):
        self.current_group_id = current_group_id
        self.current_group = current_group
        self.locations_list = locations_list if locations_list is not None else []
        self.move_character_form = move_character_form
        self.add_character_form = add_character_form
        self.add_user_form = add_user_form
        self.create_location_form = create_location_form
        self.location_map_context = location_map_context


    def get_context(self) -> dict:
        """Return context dictionary for battle rendering"""
        context = self.__dict__.copy()
        
        map_context_container = context.pop('location_map_context', None)
        
        if map_context_container:
            context.update(**map_context_container.get_context())
        
        return context