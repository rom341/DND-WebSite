from django.urls import path

from . import api
from . import views


urlpatterns = [

    path('api/location/add_character_to_location/', api.LocationApi.add_character_to_location, name='add_character_to_location')
]