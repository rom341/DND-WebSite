from django.contrib import admin

from battlefield.models import CharacterPosition, Location


# Register your models here.
admin.site.register(Location)
admin.site.register(CharacterPosition)