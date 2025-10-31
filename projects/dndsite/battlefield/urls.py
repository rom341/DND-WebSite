from django.urls import path
from . import views

urlpatterns = [
    path('battle/', views.battle, name='battle'),
    path('groups/', views.groups, name='groups'),
    path('main_page/',views.main_page, name='main_page'),
    path('', views.main_page, name='main_page'),  # Default to group selector
]