#from django import forms
from django.forms import ModelForm

from battlefield.models import Location

class CreateLocationForm(ModelForm):
    # name = forms.CharField(max_length=100)
    # description = forms.CharField(widget=forms.Textarea, required=False)
    # rows_count = forms.IntegerField(min_value=1, initial=100)
    # columns_count = forms.IntegerField(min_value=1, initial=100)
    
    
    def __init__(self, *args, **kwargs):
        super(CreateLocationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Location
        fields = [
            "name",
            "description",
            "rows_count",
            "columns_count",
            ]