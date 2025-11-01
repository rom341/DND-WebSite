from django.forms import ModelForm
from django import forms
from battlefield.models import Character

class MoveCharacterForm(ModelForm):
    class Meta:
        model = Character
        fields = ['position_x', 'position_y']
        widgets = {
            'position_x': forms.NumberInput(attrs={'min': 0, 'max': 9}),
            'position_y': forms.NumberInput(attrs={'min': 0, 'max': 4}),
        }     