from django.urls import path

from . import views, api

urlpatterns = [
    path('battlefield/', views.battlefield, name='battlefield'),
    path('battlefield/select_location/', views.select_location, name='select_location'),

    path('battlefield/get_character_positions_in_location/<int:location_id>/', api.CharacterPositionApi.get_character_positions_in_location, name='character_position_in_location_api'),
    path('battlefield/get_location/<int:location_id>/', api.CharacterPositionApi.get_location, name='location_api'),


    path('battlefield/create_location_api/', api.CharacterPositionApi.create_location, name='create_location_api'),
]