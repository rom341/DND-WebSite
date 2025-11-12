from django.contrib import admin
from groups.models import Group, GroupMembershipUser, GroupMembershipCharacter, GroupRole
# Register your models here.
admin.site.register(Group)
admin.site.register(GroupMembershipUser)
admin.site.register(GroupMembershipCharacter)
admin.site.register(GroupRole)
