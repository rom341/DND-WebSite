from django.urls import path
from . import views

urlpatterns = [    
    path('lobbys/', views.lobbys, name='lobbys'),
]