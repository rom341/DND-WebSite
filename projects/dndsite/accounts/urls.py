from django.urls import path
from . import views
from .api import app

urlpatterns = [
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.login, name='login'),
    path('accounts/main_page/',views.main_page, name='main_page'),
    path('', views.main_page, name='main_page'),  
    
    path('api/', app.urls),
]