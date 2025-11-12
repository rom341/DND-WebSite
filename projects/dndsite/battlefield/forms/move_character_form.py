from django import forms
from battlefield.models import Character
from battlefield.utils.model_managers.group_manager import GroupManager

class MoveCharacterForm(forms.ModelForm):
    name = forms.ChoiceField(label="Character")

    class Meta:
        model = Character
        fields = ['position_x', 'position_y']
        widgets = {
            'position_x': forms.NumberInput(attrs={'min': 0, 'max': 9}),
            'position_y': forms.NumberInput(attrs={'min': 0, 'max': 4}),
        }

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        super().__init__(*args, **kwargs)
        # ДОБАВИТЬ ФИЛЬТР ПРИ КОТОРОМ ИГРОК МОЖЕТ ДВИГАТЬ ТОЛЬКО СВОЕГО ПЕРСОНАЖА
        characters = GroupManager.get_characters_in_group(group) if group else Character.objects.none()
        self.fields['name'].choices = [(c.id, c.name) for c in characters]
        