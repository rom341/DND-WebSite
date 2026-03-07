from django.http import HttpResponse
from django.shortcuts import render

from lobby.models import Lobby

class CommonRequestHelper:
    @staticmethod
    def get_updated_user_list_widget(request, lobby: Lobby) -> HttpResponse:
        context = {
            'users_list': Lobby.objects.get_users_in_lobby(lobby=lobby),
        }
        return render(request, 'partials/users_list.html', context)
    
    @staticmethod
    def get_updated_battle_map_widget(request, ):
        pass