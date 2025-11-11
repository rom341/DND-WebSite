from django.contrib import admin

from battlefield.models import CharacterSkills, CharacterSpells, Group, Character, CharacterStats, CharacterMoney, GroupMembershipCharacter, GroupMembershipUser, CharacterSpellCircleSlots


# Register your models here.
admin.site.site_header = "DND Battlefield Admin"
admin.site.register(Group)
admin.site.register(GroupMembershipCharacter)
admin.site.register(GroupMembershipUser)
admin.site.register(Character)
admin.site.register(CharacterStats)
admin.site.register(CharacterMoney)
admin.site.register(CharacterSpellCircleSlots)
admin.site.register(CharacterSkills)
admin.site.register(CharacterSpells)