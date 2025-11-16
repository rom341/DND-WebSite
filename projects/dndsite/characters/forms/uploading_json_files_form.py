# my_app/forms.py

from django import forms
import json

class JsonUploadForm(forms.Form):    
    json_file = forms.FileField(
        label='Load JSON file',
    )

    def clean_json_file(self):
        """
        Custom validation for our field.
        We will check the extension and try to read the JSON.
        """
        file = self.cleaned_data.get('json_file')

        if not file:
            # If the file is not uploaded, validation fails
            raise forms.ValidationError("File was not uploaded.")

        # 1. Check the file extension
        if not file.name.endswith('.json'):
            raise forms.ValidationError("This is not a .json file.")

        # 2. Check that this is valid JSON
        # We "rewind" the file to the beginning to read it
        file.seek(0)
        try:
            # Read the file and decode it as text (utf-8)
            file_content = file.read().decode('utf-8')
            json.loads(file_content)
        except json.JSONDecodeError:
            # If json.loads() raises an error, the JSON is "broken"
            raise forms.ValidationError("Failed to parse JSON. The file is corrupted or has an invalid format.")
        except UnicodeDecodeError:
            # If the file is not in UTF-8
            raise forms.ValidationError("File encoding error. Please use UTF-8.")

        # Don't forget to rewind the file back to the beginning,
        # so it can be read in the view
        file.seek(0)
        
        # Be sure to return the "cleaned" data
        return file