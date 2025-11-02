from django.urls import path
from . import views

urlpatterns = [
    path('battle/', views.battle, name='battle'),
    path('groups/', views.groups, name='groups'),
    path('main_page/',views.main_page, name='main_page'),
    path('create_character/',views.create_character, name='create_character'),
    path('add_character_to_group/', views.add_character_to_group, name='add_character_to_group'),
    path('', views.main_page, name='main_page'),  # Default to group selector
    
]