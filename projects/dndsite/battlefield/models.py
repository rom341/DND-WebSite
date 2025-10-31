from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.username
    
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

    def __str__(self):
        return f"{self.name} (HP: {self.hit_points}, AC: {self.armor_class}, Init: {self.initiative}, Pos: ({self.position_x}, {self.position_y}))"