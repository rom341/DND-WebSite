from typing import Optional

from django.db import models
from django.contrib.auth.models import User

from core.managers.UniversalManager import UniversalManager
from lobby.models import Lobby
from location.models import Location

# Create your models here.
class CharacterSpells(models.Model):
    objects: UniversalManager = UniversalManager()
    
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
    objects: UniversalManager = UniversalManager()
    
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
    objects: UniversalManager = UniversalManager()
    
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
    objects: UniversalManager = UniversalManager()
    
    copper_coins = models.IntegerField(default=0)
    silver_coins = models.IntegerField(default=0)
    electrum_coins = models.IntegerField(default=0)
    gold_coins = models.IntegerField(default=0)
    platinum_coins = models.IntegerField(default=0)

    def __str__(self):
        return f"ID{self.id}: {self.copper_coins} CC, {self.silver_coins} SC, {self.electrum_coins} EC, {self.gold_coins} GC, {self.platinum_coins} PC"

class CharacterStats(models.Model):
    objects: UniversalManager = UniversalManager()
    
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


class EntityBaseController(UniversalManager):
    def create_entity_base(self,                            
        entity_base_name:str,
        character_class:str = None,
        race:str = None,
        alignment:str = None,
        size:str = None,
        age:int = None,
        height:str = None,
        weight:str = None,
        mastery:int = 0
        ):
        return self.create(
            entity_base_name = entity_base_name,
            character_class = character_class,
            race = race,
            alignment = alignment,
            size = size,
            age = age,
            height = height,
            weight = weight,
            mastery = mastery
        )
    
    def get_by_id(self, id: int):
        return EntityBase.objects.get(id=id)
    
    def get_all_entity_bases(self):
        return EntityBase.objects.all()
    
    def create_npc(self, user: User, entity_base: "EntityBase", count: int = 1):
        created = []
        for i in range(count):
            created.append(Character.objects.create_character_for_npc(user, entity_base))
        return created

class EntityBase(models.Model):
    objects: EntityBaseController = EntityBaseController()

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

class HealActionType:
    Heal = 1
    Damage = 2

    Choices = [
        (Heal, "Heal"),
        (Damage, "Damage")
    ]

class CharacterController(UniversalManager):
    def get_character_by_id(self, character_id: int):
        return Character.objects.get(id=character_id)
    
    def create_character(
        self,
        user: User,
        character_name: str,
        entity_base_id: int,
        level: int = 1,
        experience: int = 0,
        max_hit_points: int = 0,
        is_npc: bool = False,
        money: CharacterMoney = None,
        stats: CharacterStats = None,
        spell_circle_slots: CharacterSpellCircleSlots = None
        ):
        return self.create(user=user, character_name=character_name, entity_base_id=entity_base_id, level=level, experience=experience, max_hit_points=max_hit_points, is_npc=is_npc, money=money, stats=stats, spell_circle_slots=spell_circle_slots)
        
    def create_character_for_npc(
            self,
            user: User,
            entity_base: EntityBase           
        ):
        return self.create_character(
            user,
            f"npc_{entity_base.entity_base_name}",
            entity_base.id,
            max_hit_points=entity_base.max_hit_points,
            is_npc=True
        )
    
    def get_characters_available_for_user_in_location(
            self,
            user: User,
            location: "Location",
        ):
        from location.models import Location
        from lobby.models import DefaultRoles, LobbyRole

        if LobbyRole.objects.user_has_role(user=user, lobby=location.lobby, role=DefaultRoles.GAME_MASTER):
            return Location.objects.get_characters_in_location(location=location)
        else:        
            return Location.objects.get_characters_in_location_for_user(user=user, location=location)
        
    def change_health(
            self,
            character: 'Character',
            heal_value: int,
            heal_type: int
    ):
        if not character:
            return
        
        health_change_value = heal_value * -1 if heal_type == HealActionType.Heal else 1

        new_health = max(-10000, min(character.current_hit_points + health_change_value, character.entity_base.max_hit_points))
        character.current_hit_points = new_health
        character.save()

class Character(models.Model):
    objects: CharacterController = CharacterController()
    
    user = models.ForeignKey(User, related_name='characters', on_delete=models.CASCADE)
    character_name = models.CharField(max_length=100)
    entity_base = models.ForeignKey(EntityBase, related_name='character', on_delete=models.CASCADE, null=True, blank=True)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    max_hit_points = models.IntegerField(default=0)
    armor_class = models.IntegerField(default=0)
    movement_speed = models.IntegerField(default=0)
    is_npc = models.BooleanField(default=False)
    money = models.ForeignKey(CharacterMoney, related_name='character', on_delete=models.CASCADE, null=True, blank=True)
    stats = models.ForeignKey(CharacterStats, related_name='character', on_delete=models.CASCADE, null=True, blank=True)
    spell_circle_slots = models.ForeignKey(CharacterSpellCircleSlots, related_name='character', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"ID{self.id}: {self.character_name} (HP: {self.max_hit_points}, AC: {self.armor_class}, MS: {self.movement_speed})"
        
class CharacterStateController(UniversalManager):
    def create_character_state(self, character: Character, lobby: Lobby):
        return self.create(
            character=character,
            lobby=lobby,
            current_hit_points=character.max_hit_points
        )
        
class CharacterState(models.Model):
    objects: CharacterStateController = CharacterStateController()
    
    character = models.ForeignKey(Character, related_name='states', on_delete=models.CASCADE)
    lobby = models.ForeignKey(Lobby, related_name='character_states', on_delete=models.CASCADE)
    current_hit_points = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('character', 'lobby')
    
class CharacterPositionController(UniversalManager):
    def create_character_position(self, character_state: CharacterState, location: Location, row: int, column: int) -> 'CharacterPosition':
        character_position = CharacterPosition.objects.create(
            character_state=character_state, 
            location=location,
            row=row,
            column=column
        )
        return character_position
    
    def set_character_position(self, character_state: CharacterState, location: Location, row: int, column: int) -> 'CharacterPosition':
        character_position = CharacterPosition.objects.get(character_state=character_state, location=location)
        character_position.row = row
        character_position.column = column
        character_position.save()
        return character_position
    
    def get_character_position_in_location(self, character: Character, location: Location) -> Optional["CharacterPositionController"]:
        try:
            return CharacterPosition.objects.get(character_state__character=character, location=location)
        except CharacterPosition.DoesNotExist:
            return None
        
    def get_all_character_positions_in_location(self, location: Location) -> "CharacterPositionController":
        return CharacterPosition.objects.filter(location=location)
    
    def get_all_character_positions_in_location_by_id(self, location_id: int) -> "CharacterPositionController":
        return CharacterPosition.objects.filter(location__id=location_id)
    
    def move_character(self, character: Character, location: Location, new_row: int, new_column: int) -> Optional["CharacterPosition"]:
        character_position = self.get_character_position_in_location(character, location)
        if character_position:
            character_position.row = new_row
            character_position.column = new_column
            character_position.save()
            return character_position
        return None
    
    def is_position_occupied(self, location: Location, row: int, column: int) -> bool:
        return CharacterPosition.objects.filter(location=location, row=row, column=column).exists()
    
class CharacterPosition(models.Model):
    objects: CharacterPositionController = CharacterPositionController()
    character_state = models.ForeignKey(CharacterState, on_delete=models.CASCADE, related_name='position')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='character_positions')
    row = models.IntegerField(default=0)
    column = models.IntegerField(default=0)

    class Meta:
        unique_together = ('character_state', 'location')

    def __str__(self):
        return f"{self.character_state.character.character_name} at ({self.row}, {self.column}) in {self.location.name}"
    