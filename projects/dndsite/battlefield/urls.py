from django.urls import path
from . import views

urlpatterns = [
    path('battle/', views.battle, name='battle'),
]