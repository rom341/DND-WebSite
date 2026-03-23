from django import forms
from django.db.models import QuerySet
from battlefield.models import CharacterPosition
from characters.models import Character

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
        available_characters = kwargs.pop("available_characters", Character.objects.none())
        super().__init__(*args, **kwargs)
        characters = available_characters if available_characters is not None else Character.objects.none()
        self.fields['name'].choices = [(c.id, c.character_name) for c in characters]
        