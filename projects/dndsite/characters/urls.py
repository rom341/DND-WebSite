from django.urls import path
from . import views

urlpatterns = [    
    path('characters/create_character/',views.create_character, name='create_character'),
    path('characters/create_skill/',views.create_skill, name='create_skill'),
    path('characters/create_spell/',views.create_spell, name='create_spell'),
    path('characters/upload_json/', views.upload_longstory_character_json, name='upload_json'),
    path('characters/my_characters_list/', views.my_characters_list, name='my_characters_list'),
    path('characters/heal_cahracter/', views.heal_character, name='heal_character'),
]