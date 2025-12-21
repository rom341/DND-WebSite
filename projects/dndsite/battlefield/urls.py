from django.urls import path
from . import views

urlpatterns = [
    path('battlefield/', views.battlefield, name='battlefield'),
    path('add_character_to_lobby/', views.add_character_to_lobby, name='add_character_to_lobby'),
    path('add_user_to_lobby/', views.add_user_to_lobby, name='add_user_to_lobby'),
    path('create_location/', views.create_location, name='create_location'),
    path('select_location/', views.select_location, name='select_location'),
]