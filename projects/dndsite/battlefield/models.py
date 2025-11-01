from django.db import models
from django.contrib.auth.models import User

# Create your models here.    
class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class CharacterStats(models.Model):
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
    temp = models.IntegerField(default=0)

class Character(models.Model):
    user = models.ForeignKey(User, related_name='characters', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, related_name='characters', on_delete=models.CASCADE, null=True, blank=True)
    stats = models.ForeignKey(CharacterStats, related_name='character', on_delete=models.CASCADE, null=True, blank=True)
    max_hit_points = models.IntegerField(default=0)
    current_hit_points = models.IntegerField(default=0)
    armor_class = models.IntegerField(default=0)
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)
    movement_speed = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['group', 'position_x', 'position_y'], 
                name='unique_position_in_group'
            )
        ]

    def __str__(self):
        return f"ID{self.id}: {self.name} (HP: {self.max_hit_points}, AC: {self.armor_class}, Pos: ({self.position_x}, {self.position_y}))"
    
    def move_to(self, new_x, new_y):
        self.position_x = new_x
        self.position_y = new_y
        self.save()