class LocationMapContextContainer:
    def __init__(self, current_location_id=None, current_location=None, rows_count=0, cols_count=0, 
                 characters_list=None, character_position_context=None
                 ):
        self.current_location_id = current_location_id
        self.current_location = current_location
        self.rows_count = rows_count
        self.cols_count = cols_count
        self.rows_range = range(self.rows_count)
        self.cols_range = range(self.cols_count)
        self.characters_list = characters_list if characters_list is not None else []
        self.character_position_context = character_position_context

    def get_context(self):
        context = self.__dict__.copy()
        map_context_container = context.pop('character_position_context', None)
        
        if map_context_container:
            context.update(**map_context_container.get_context())
        
        return context
