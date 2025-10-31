from django.contrib import admin

from battlefield.models import Group, Character


# Register your models here.
admin.site.site_header = "DND Battlefield Admin"
admin.site.register(Group)
admin.site.register(Character)