from django import forms
from django.contrib.auth.models import User

from lobby.models import Lobby

class AddUserToLobbyForm(forms.Form):
    user_id = forms.ModelChoiceField(queryset=User.objects.all(), label="User")
    
    def __init__(self, *args, **kwargs):
        lobby = kwargs.pop('lobby', None)
        super().__init__(*args, **kwargs)
        if lobby:
            users = Lobby.objects.get_users_in_lobby(lobby)
            existing_user_ids = users.values_list('id', flat=True)
            self.fields['user_id'].queryset = User.objects.exclude(id__in=existing_user_ids)
        else:
            self.fields['user_id'].queryset = User.objects.none()