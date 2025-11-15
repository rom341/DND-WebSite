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

    def __init__(self, available_characters=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        available_characters = available_characters
        characters = available_characters if available_characters is not None else Character.objects.none()
        self.fields['name'].choices = [(c.id, c.name) for c in characters]
        