from django.urls import path

from . import api
from .api import app
from . import views


urlpatterns = [
    path('api/', app.urls),
]