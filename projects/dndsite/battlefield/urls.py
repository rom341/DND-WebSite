from django.urls import path

from . import views, api

urlpatterns = [
    path('battlefield/', views.battlefield, name='battlefield'),
    path('battlefield/add_character_to_lobby/', views.add_character_to_lobby, name='add_character_to_lobby'),
    path('battlefield/add_npc_to_lobby/', views.add_npc_to_lobby, name='add_npc_to_lobby'),
    path('battlefield/add_user_to_lobby/', views.add_user_to_lobby, name='add_user_to_lobby'),
    path('battlefield/create_location/', views.create_location, name='create_location'),
    path('battlefield/select_location/', views.select_location, name='select_location'),

    path('battlefield/character_position_in_location/<int:location_id>/', api.CharacterPositionApi.get_characters_in_location, name='character_position_in_location_api')
]