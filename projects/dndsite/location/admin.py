from django.contrib import admin
from location.models import CharacterPosition, Location

# Register your models here.
admin.site.register(Location)
admin.site.register(CharacterPosition)