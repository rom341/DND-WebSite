from django import forms
from django.db.models import QuerySet
from battlefield.models import Location
from characters.models import EntityBase
from lobby.models import Lobby

class AddNPCToLobbyForm(forms.Form):
    entity_base = forms.ModelChoiceField(queryset=None, label="Entity base")
    location = forms.ModelChoiceField(queryset=None, label="Location")
    count = forms.IntegerField(max_value=30, label="Count")
    
    def __init__(self, *args, **kwargs):
        lobby = kwargs.pop('lobby', None)
        super().__init__(*args, **kwargs)
        if lobby:
            entities = EntityBase.objects.get_all_entity_bases()
            self.fields['entity_base'].queryset = entities
            self.fields['location'].queryset = Location.objects.get_locations_for_lobby(lobby)
        else:
            self.fields['entity_base'].queryset = EntityBase.objects.none()
            self.fields['location'].queryset = Location.objects.none()