from django.urls import path

from lobby import api
from . import views

urlpatterns = [    
    path('lobby/', views.lobby, name='lobby'),
    path('lobby/add_character_to_lobby/', views.add_character_to_lobby, name='add_character_to_lobby'),
    path('lobby/add_npc_to_lobby/', views.add_npc_to_lobby, name='add_npc_to_lobby'),    
    #path('lobby/add_user_to_lobby/', views.add_user_to_lobby, name='add_user_to_lobby'),

    path('lobby/get_locations_for_lobby/<int:lobby_id>/', api.LobbyApi.get_locations_for_lobby, name='get_locations_for_lobby'),
    path('lobby/get_lobby/<int:lobby_id>/', api.LobbyApi.get_lobby, name='get_lobby'),
    
    path('api/lobby/add_user_to_lobby/', api.LobbyApi.add_user_to_lobby, name='add_user_to_lobby')
    path('api/lobby/add_character_to_lobby/', api.LobbyApi.add_character_to_lobby, name='add_character_to_lobby')
]