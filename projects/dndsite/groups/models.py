from enum import Enum
from django.db import models
from django.contrib.auth.models import User

from characters.models import Character

# Create your models here.
class DefaultRoles(Enum):
    GAME_MASTER = 'GM'
    PLAYER = 'Player'

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class GroupRole(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class GroupMembershipUser(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='user_memberships')
    role = models.ForeignKey(GroupRole, on_delete=models.CASCADE, related_name='memberships')

    class Meta:
        unique_together = ('user', 'group')
        
    def __str__(self):
        return f"{self.user.username} ({self.role}) in {self.group.name}"

class GroupMembershipCharacter(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='group_memberships')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='character_memberships')

    class Meta:
        unique_together = ('character', 'group')

    def __str__(self):
        return f"{self.character.name} in {self.group.name}"