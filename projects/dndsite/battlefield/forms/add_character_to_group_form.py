from django import forms
from battlefield.models import Location
from battlefield.utils.managers.location_manager import LocationManager
from characters.models import Character
from groups.utils.managers.group_manager import GroupManager

class AddCharacterToGroupForm(forms.Form):
    character_id = forms.ModelChoiceField(queryset=None, label="Character")
    location_id = forms.ModelChoiceField(queryset=None, label="Location")
    target_row = forms.IntegerField(label="Target Row (Y Coordinate)")
    target_column = forms.IntegerField(label="Target Column (X Coordinate)")
    
    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        super().__init__(*args, **kwargs)
        if group:
            users_in_group = GroupManager.get_users_in_group(group)
            characters_in_group = GroupManager.get_characters_in_group(group)
            character_in_group_ids = characters_in_group.values_list('id', flat=True)
            
            # Filter characters to only those whose users are in the group and not already in the group
            self.fields['character_id'].queryset = Character.objects.filter(user__in=users_in_group).exclude(id__in=character_in_group_ids)
            self.fields['location_id'].queryset = LocationManager.get_locations_for_group(group)
        else:
            self.fields['character_id'].queryset = Character.objects.none()
            self.fields['location_id'].queryset = Location.objects.none()