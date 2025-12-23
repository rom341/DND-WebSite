from django.contrib import admin

from characters.models import Character, EntityBase, CharacterStats, CharacterMoney, CharacterSpellCircleSlots, CharacterSkills, CharacterSpells

# Register your models here.
admin.site.register(CharacterStats)
admin.site.register(CharacterMoney)
admin.site.register(CharacterSpellCircleSlots)
admin.site.register(CharacterSkills)
admin.site.register(CharacterSpells)
admin.site.register(EntityBase)
admin.site.register(Character)