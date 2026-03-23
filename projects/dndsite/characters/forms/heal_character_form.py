from django import forms
from characters.models import Character, HealActionType
from django.db import models

class HealCharacterForm(forms.Form):
    character = forms.ModelChoiceField(queryset=Character.objects.none(), label="Character")
    heal_action_type = forms.ChoiceField(choices=HealActionType.Choices, label="Action Type")
    health_value = forms.IntegerField(min_value=0, label="Value")

    def __init__(self, *args, **kwargs):
        available_characters = kwargs.pop("available_characters", Character.objects.none())
        super().__init__(*args, **kwargs)
        self.fields['character'].queryset = available_characters