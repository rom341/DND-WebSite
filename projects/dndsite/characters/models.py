from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UniversalManager(models.Manager):
    def create_from_template(self, template):
        field_names = [f.name for f in self.model._meta.fields if not f.primary_key]
        stats_data = {field: getattr(template, field) for field in field_names if hasattr(template, field)}        
        return self.create(**stats_data)


class CharacterSpells(models.Model):
    objects = UniversalManager()
    
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
    objects = UniversalManager()
    
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
    objects = UniversalManager()
    
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
    objects = UniversalManager()
    
    copper_coins = models.IntegerField(default=0)
    silver_coins = models.IntegerField(default=0)
    electrum_coins = models.IntegerField(default=0)
    gold_coins = models.IntegerField(default=0)
    platinum_coins = models.IntegerField(default=0)

    def __str__(self):
        return f"ID{self.id}: {self.copper_coins} CC, {self.silver_coins} SC, {self.electrum_coins} EC, {self.gold_coins} GC, {self.platinum_coins} PC"

class CharacterStats(models.Model):
    objects = UniversalManager()
    
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

class EntityBase(models.Model):
    objects = UniversalManager()

    entity_base_name = models.CharField(max_length=100)
    character_class = models.CharField(max_length=15, null=True, blank=True)
    character_sub_class = models.CharField(max_length=15, null=True, blank=True)
    race = models.CharField(max_length=50, null=True, blank=True)
    alignment = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    height = models.CharField(max_length=20, null=True, blank=True)
    weight = models.CharField(max_length=20, null=True, blank=True)
    mastery = models.IntegerField(default=0)
    dificulty_save_throw = models.IntegerField(default=0)
    max_hit_points = models.IntegerField(default=0)
    armor_class = models.IntegerField(default=0)
    movement_speed = models.IntegerField(default=0)

    def __str__(self):
            fields = [f"{field.name}: {getattr(self, field.name)}" for field in self._meta.fields]
            return f"EntityBase({', '.join(fields)})"

    def is_equal_to_template(self, template):
        field_names = [f.name for f in self._meta.fields if not f.primary_key]
        
        stats_data = []
        for field in field_names:
            if hasattr(template, field):
                val_self = getattr(self, field)
                val_temp = getattr(template, field)

                if val_self is None: val_self = ''
                if val_temp is None: val_temp = ''

                is_equal = str(val_self).strip() == str(val_temp).strip()
                
                stats_data.append(is_equal)
                
                # print(f"Field: {field} | Base: {val_self} ({type(val_self)}) | Temp: {val_temp} ({type(val_temp)}) | Match: {is_equal}")
        return all(stats_data)

class Character(models.Model):
    objects = UniversalManager()
    
    user = models.ForeignKey(User, related_name='characters', on_delete=models.CASCADE)
    character_name = models.CharField(max_length=100)
    entity_base = models.ForeignKey(EntityBase, related_name='character', on_delete=models.CASCADE, null=True, blank=True)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    current_hit_points = models.IntegerField(default=0)
    money = models.ForeignKey(CharacterMoney, related_name='character', on_delete=models.CASCADE, null=True, blank=True)
    stats = models.ForeignKey(CharacterStats, related_name='character', on_delete=models.CASCADE, null=True, blank=True)
    spell_circle_slots = models.ForeignKey(CharacterSpellCircleSlots, related_name='character', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"ID{self.id}: {self.character_name} (HP: {self.entity_base.max_hit_points}, AC: {self.entity_base.armor_class})"
        