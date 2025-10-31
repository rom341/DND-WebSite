from django.urls import path
from . import views

urlpatterns = [
    path('battle/', views.battle, name='battle'),
    path('groups/', views.groups, name='groups'),
    path('main/',views.main, name='main'),
    path('', views.groups, name='groups'),  # Default to group selector
]