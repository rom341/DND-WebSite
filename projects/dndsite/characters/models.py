from django.db import models
from django.contrib.auth.models import User

from characters.templates import CharacterSpellsTemplate, CharacterSkillsTemplate, CharacterSpellCirclesSlotsTemplate, CharacterMoneyTemplate, CharacterStatsTemplate, CharacterTemplate

# Create your models here.
class CharacterSpells(models.Model):
    def create_from_template(self, template:CharacterSpellsTemplate):
        self.spell_name = template.spell_name
        self.atack_roll = template.atack_roll
        self.damage_dice = template.damage_dice
        self.damage_dice_count = template.damage_dice_count
        self.damage_modificator = template.damage_modificator
        self.saving_throw = template.saving_throw
        self.is_using_spell_circle = template.is_using_spell_circle
        self.required_spell_circle = template.required_spell_circle
        self.save()
        return self
    
    spell_name = models.CharField(max_length=50)
    atack_roll = models.CharField(max_length=10)
    damage_dice = models.CharField(max_length=10)
    damage_dice_count = models.IntegerField(default=1)
    damage_modificator = models.IntegerField(default=0)
    saving_throw = models.CharField(max_length=5)
    is_using_spell_circle = models.BooleanField(default=True)
    required_spell_circle = models.IntegerField(default=1)

    def __str__(self):
         return f"ID{self.id}: {self.spell_name}"


class CharacterSkills(models.Model):
    def create_from_template(self, template:CharacterSkillsTemplate):
        self.skill_name = template.skill_name
        self.atack_roll = template.atack_roll
        self.damage_dice = template.damage_dice
        self.damage_dice_count = template.damage_dice_count
        self.damage_modificator = template.damage_modificator
        self.saving_throw = template.saving_throw
        self.is_using_spell_circle = template.is_using_spell_circle
        self.required_spell_circle = template.required_spell_circle
        self.save()
        return self
    
    skill_name = models.CharField(max_length=50)
    atack_roll = models.CharField(max_length=10)
    damage_dice = models.CharField(max_length=10)
    damage_dice_count = models.IntegerField(default=1)
    damage_modificator = models.IntegerField(default=0)
    saving_throw = models.CharField(max_length=5)
    is_using_spell_circle = models.BooleanField(default=False)
    required_spell_circle = models.IntegerField(default=1)

    def __str__(self):
         return f"ID{self.id}: {self.skill_name}"

class CharacterSpellCircleSlots(models.Model):
    def create_from_template(self, template:CharacterSpellCirclesSlotsTemplate):
        self.circle_1 = template.circle_1
        self.circle_2 = template.circle_2
        self.circle_3 = template.circle_3
        self.circle_4 = template.circle_4
        self.circle_5 = template.circle_5
        self.circle_6 = template.circle_6
        self.circle_7 = template.circle_7
        self.circle_8 = template.circle_8
        self.circle_9 = template.circle_9
        self.save()
        return self
    
    circle_1 = models.IntegerField(default=0)
    circle_2 = models.IntegerField(default=0)
    circle_3 = models.IntegerField(default=0)
    circle_4 = models.IntegerField(default=0)
    circle_5 = models.IntegerField(default=0)
    circle_6 = models.IntegerField(default=0)
    circle_7 = models.IntegerField(default=0)
    circle_8 = models.IntegerField(default=0)
    circle_9 = models.IntegerField(default=0)

    def __str__(self):
        return f"ID{self.id}: Circles Slots - 1:{self.circle_1}, 2:{self.circle_2}, 3:{self.circle_3}, 4:{self.circle_4}, 5:{self.circle_5}, 6:{self.circle_6}, 7:{self.circle_7}, 8:{self.circle_8}, 9:{self.circle_9}"
    
class CharacterMoney(models.Model):
    def create_from_template(self, template:CharacterMoneyTemplate):
        self.copper_coins = template.copper_coins
        self.silver_coins = template.silver_coins
        self.electrum_coins = template.electrum_coins
        self.gold_coins = template.gold_coins
        self.platinum_coins = template.platinum_coins
        self.save()
        return self
    
    copper_coins = models.IntegerField(default=0)
    silver_coins = models.IntegerField(default=0)
    electrum_coins = models.IntegerField(default=0)
    gold_coins = models.IntegerField(default=0)
    platinum_coins = models.IntegerField(default=0)

    def __str__(self):
        return f"ID{self.id}: {self.copper_coins} CC, {self.silver_coins} SC, {self.electrum_coins} EC, {self.gold_coins} GC, {self.platinum_coins} PC"

class CharacterStats(models.Model):
    def create_from_template(self, template:CharacterStatsTemplate):
        self.strength = template.strength
        self.dexterity = template.dexterity
        self.constitution = template.constitution
        self.intelligence = template.intelligence
        self.wisdom = template.wisdom
        self.charisma = template.charisma
        self.save()
        return self
    
    strength = models.IntegerField(default=0)
    """Main character stat СИЛА"""
    dexterity = models.IntegerField(default=0)
    """Main character stat ЛОВКОСТЬ"""
    constitution = models.IntegerField(default=0)
    """Main character stat ТЕЛОСЛОЖЕНИЕ"""
    intelligence = models.IntegerField(default=0)
    """Main character stat ИНТЕЛЛЕКТ"""
    wisdom = models.IntegerField(default=0)
    """Main character stat МУДРОСТЬ"""
    charisma = models.IntegerField(default=0)
    """Main character stat ХАРИЗМА"""
    
    def __str__(self):
        return f"ID{self.id}: str {self.strength}, dex {self.dexterity}, con {self.constitution}, int  {self.intelligence}, wis {self.wisdom}, cha {self.charisma}"

class Character(models.Model):
    def create_form_template(self, template:CharacterTemplate):
        self.name = template.character_name
        self.character_class = template.character_class
        self.character_sub_class = template.character_sub_class
        self.level = template.level
        self.experience = template.experience
        self.race = template.race
        self.alignment = template.alignment
        self.size = template.size
        self.age = template.age
        self.height = template.height
        self.weight = template.weight
        self.max_hit_points = template.max_hit_points
        self.current_hit_points = template.current_hit_points
        self.armor_class = template.armor_class
        self.movement_speed = template.movement_speed
        if template.character_stats_template:
            new_stats = CharacterStats()
            stats = new_stats.create_from_template(template.character_stats_template)
            self.stats = stats
        if template.character_money_template:
            new_money_bag = CharacterMoney()
            money = new_money_bag.create_from_template(template.character_money_template)
            self.money = money
        if template.character_spell_circle_slots_template:
            new_spell_slots = CharacterSpellCircleSlots()
            spell_circle_slots = new_spell_slots.create_from_template(template.character_spell_circle_slots_template)
            self.spell_circle_slots = spell_circle_slots   
        self.save()
        return self
    
    user = models.ForeignKey(User, related_name='characters', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    stats = models.ForeignKey(CharacterStats, related_name='character', on_delete=models.CASCADE, null=True, blank=True)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    race = models.CharField(max_length=50, null=True, blank=True)
    alignment = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    height = models.CharField(max_length=20, null=True, blank=True)
    weight = models.CharField(max_length=20, null=True, blank=True)
    movement_speed = models.IntegerField(default=0)
    max_hit_points = models.IntegerField(default=0)
    current_hit_points = models.IntegerField(default=0)
    character_class = models.CharField(max_length=15, null=True, blank=True)
    character_sub_class = models.CharField(max_length=15, null=True, blank=True)
    armor_class = models.IntegerField(default=0)
    money = models.ForeignKey(CharacterMoney, related_name='character', on_delete=models.CASCADE, null=True, blank=True)
    spell_circle_slots = models.ForeignKey(CharacterSpellCircleSlots, related_name='character', on_delete=models.CASCADE, null=True, blank=True)
    mastery = models.IntegerField(default=2)
    dificulty_save_throw = models.IntegerField(default=0)


    def __str__(self):
        return f"ID{self.id}: {self.name} (HP: {self.max_hit_points}, AC: {self.armor_class})"
    