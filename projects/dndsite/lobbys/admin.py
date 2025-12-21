from django.contrib import admin
from lobbys.models import Lobby, LobbyMembershipUser, LobbyMembershipCharacter, LobbyRole
# Register your models here.
admin.site.register(Lobby)
admin.site.register(LobbyMembershipUser)
admin.site.register(LobbyMembershipCharacter)
admin.site.register(LobbyRole)
