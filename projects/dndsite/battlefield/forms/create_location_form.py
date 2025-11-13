from django import forms

class CreateLocationForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea, required=False)
    rows_count = forms.IntegerField(min_value=1, initial=100)
    columns_count = forms.IntegerField(min_value=1, initial=100)
    
    group = None
    
    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group', None)
        super(CreateLocationForm, self).__init__(*args, **kwargs)