from django.db import models

from characters.models import Character
from groups.models import Group

# Create your models here.    
class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    rows_count = models.IntegerField(default=10)
    columns_count = models.IntegerField(default=10)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='locations')

    def __str__(self):
        return f"{self.name} ({self.rows_count}x{self.columns_count})"
    
class CharacterPosition(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='positions')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='character_positions')
    row = models.IntegerField(default=0)
    column = models.IntegerField(default=0)

    class Meta:
        unique_together = ('character', 'location')

    def __str__(self):
        return f"{self.character.name} at ({self.row}, {self.column}) in {self.location.name}"