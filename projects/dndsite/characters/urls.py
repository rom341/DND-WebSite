from django.urls import path
from . import views

urlpatterns = [    
    path('create_character/',views.create_character, name='create_character'),
    path('create_skill/',views.create_skill, name='create_skill'),
    path('create_spell/',views.create_spell, name='create_spell'),
    path('upload_json/', views.upload_longstory_character_json, name='upload_json'),
    path('my_characters_list/', views.my_characters_list, name='my_characters_list'),
]