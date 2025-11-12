from django import forms
from django.contrib.auth.models import User
from groups.utils.managers.group_manager import GroupManager

class AddUserToGroupForm(forms.Form):
    user_id = forms.ModelChoiceField(queryset=User.objects.all(), label="User")
    
    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        super().__init__(*args, **kwargs)
        if group:
            users = GroupManager.get_users_in_group(group)
            existing_user_ids = users.values_list('id', flat=True)
            self.fields['user_id'].queryset = User.objects.exclude(id__in=existing_user_ids)
        else:
            self.fields['user_id'].queryset = User.objects.none()