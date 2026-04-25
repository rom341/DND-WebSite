from django.forms import ModelForm
from characters.models import EntityBase

class EntityBaseForm(ModelForm):
    class Meta:
        model = EntityBase
        fields = [
            "entity_base_name",
            "character_class",
            "character_sub_class",
            "race",
            "alignment",
            "size",
            "age",
            "height",
            "weight",
            "mastery",
            ]