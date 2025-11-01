from django.db import models
from django.contrib.auth.models import User

# Create your models here.    
class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Character(models.Model):
    user = models.ForeignKey(User, related_name='characters', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, related_name='characters', on_delete=models.CASCADE)
    hit_points = models.IntegerField(default=0)
    armor_class = models.IntegerField(default=0)
    initiative = models.IntegerField(default=0)
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['group', 'position_x', 'position_y'], 
                name='unique_position_in_group'
            )
        ]

    def __str__(self):
        return f"ID{self.id}: {self.name} (HP: {self.hit_points}, AC: {self.armor_class}, Init: {self.initiative}, Pos: ({self.position_x}, {self.position_y}))"