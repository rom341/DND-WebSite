from django import forms
from characters.models import Character
from groups.utils.managers.group_manager import GroupManager

class AddCharacterToGroupForm(forms.Form):
    character_id = forms.ModelChoiceField(queryset=Character.objects.all(), label="Character")
    
    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        super().__init__(*args, **kwargs)
        if group:
            characters = GroupManager.get_characters_in_group(group)
            existing_character_ids = characters.values_list('id', flat=True)
            self.fields['character_id'].queryset = Character.objects.exclude(id__in=existing_character_ids)
        else:
            self.fields['character_id'].queryset = Character.objects.none()