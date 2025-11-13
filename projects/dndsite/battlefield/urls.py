from django.urls import path
from . import views

urlpatterns = [
    path('battlefield/', views.battlefield, name='battlefield'),
    path('add_character_to_group/', views.add_character_to_group, name='add_character_to_group'),
    path('add_user_to_group/', views.add_user_to_group, name='add_user_to_group'),
    path('create_location/', views.create_location, name='create_location'),
    path('select_location/', views.select_location, name='select_location'),
]