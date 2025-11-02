from django.contrib import admin

from battlefield.models import Group, Character, CharacterStats, CharacterMoney, GroupMembershipCharacter, GroupMembershipUser


# Register your models here.
admin.site.site_header = "DND Battlefield Admin"
admin.site.register(Group)
admin.site.register(GroupMembershipCharacter)
admin.site.register(GroupMembershipUser)
admin.site.register(Character)
admin.site.register(CharacterStats)
admin.site.register(CharacterMoney)