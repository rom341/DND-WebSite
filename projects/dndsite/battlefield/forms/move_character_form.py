from django import forms
from battlefield.models import CharacterPosition
from battlefield.utils.managers.location_manager import LocationManager
from characters.models import Character
from groups.utils.managers.group_manager import GroupManager

class MoveCharacterForm(forms.ModelForm):
    name = forms.ChoiceField(label="Character")

    class Meta:
        model = CharacterPosition
        fields = ['column', 'row']
        widgets = {
            'column': forms.NumberInput(attrs={'min': 0, 'max': 100}),
            'row': forms.NumberInput(attrs={'min': 0, 'max': 100}),
        }

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        location = kwargs.pop('location', None)
        super().__init__(*args, **kwargs)
        #characters = GroupManager.get_characters_in_group(group) if group else Character.objects.none()
        characters = LocationManager.get_characters_in_location(location) if location else Character.objects.none()
        self.fields['name'].choices = [(c.id, c.name) for c in characters]
        