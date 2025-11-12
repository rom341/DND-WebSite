from django.urls import path
from . import views

urlpatterns = [
    path('battle/', views.battle, name='battle'),
    path('add_character_to_group/', views.add_character_to_group, name='add_character_to_group'),
    path('add_user_to_group/', views.add_user_to_group, name='add_user_to_group'),
    
]