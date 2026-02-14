from django import forms
from battlefield.models import Location
from characters.models import Character
from lobby.models import Lobby

class AddCharacterToGroupForm(forms.Form):
    character_id = forms.ModelChoiceField(queryset=None, label="Character")
    location_id = forms.ModelChoiceField(queryset=None, label="Location")
    target_row = forms.IntegerField(label="Target Row (Y Coordinate)")
    target_column = forms.IntegerField(label="Target Column (X Coordinate)")
    
    def __init__(self, *args, **kwargs):
        lobby = kwargs.pop('lobby', None)
        super().__init__(*args, **kwargs)
        if lobby:
            users_in_lobby = Lobby.objects.get_users_in_lobby(lobby)
            characters_in_lobby = Lobby.objects.get_characters_in_lobby(lobby)
            character_in_lobby_ids = characters_in_lobby.values_list('id', flat=True)
            
            # Filter characters to only those whose users are in the lobby and not already in the lobby
            self.fields['character_id'].queryset = Character.objects.filter(user__in=users_in_lobby).exclude(id__in=character_in_lobby_ids)
            self.fields['location_id'].queryset = Location.objects.get_locations_for_lobby(lobby)
        else:
            self.fields['character_id'].queryset = Character.objects.none()
            self.fields['location_id'].queryset = Location.objects.none()