from django import forms
from battlefield.models import Location
from characters.models import EntityBase

class AddNPCToLobbyForm(forms.Form):
    entity_base_id = forms.ModelChoiceField(queryset=None, label="Entity base")
    location_id = forms.ModelChoiceField(queryset=None, label="Location")
    count = forms.IntegerField(max_value=30, label="Count")
    
    def __init__(self, *args, **kwargs):
        lobby = kwargs.pop('lobby', None)
        super().__init__(*args, **kwargs)
        if lobby:
            entities = EntityBase.objects.get_all_character_model_templates()
            #entity_ids = entities.values_list('id', flat=True)
            
            # Filter characters to only those whose users are in the lobby and not already in the lobby
            self.fields['entity_base_id'].queryset = entities
            self.fields['location_id'].queryset = Location.objects.get_locations_for_lobby(lobby)
        else:
            self.fields['entity_base_id'].queryset = EntityBase.objects.none()
            self.fields['location_id'].queryset = Location.objects.none()