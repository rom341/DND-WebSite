class LocationsListContextContainer:
    """Class to encapsulate battle context data"""
    def __init__(self, locations_list=None):
        self.locations_list = locations_list if locations_list is not None else []


    def get_context(self) -> dict:
        """Return context dictionary for battle rendering"""
        return self.__dict__.copy()