from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('main_page/',views.main_page, name='main_page'),
    path('', views.main_page, name='main_page'),  
]