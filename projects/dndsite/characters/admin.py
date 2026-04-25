from django.contrib import admin

from characters.models import EntityBase, Character, CharacterState, CharacterPosition 
from characters.models import CharacterStats, CharacterMoney, CharacterSpellCircleSlots, CharacterSkills, CharacterSpells

# Register your models here.
admin.site.register(CharacterStats)
admin.site.register(CharacterMoney)
admin.site.register(CharacterSpellCircleSlots)
admin.site.register(CharacterSkills)
admin.site.register(CharacterSpells)
admin.site.register(EntityBase)
admin.site.register(Character)
admin.site.register(CharacterState)
admin.site.register(CharacterPosition)