from django.contrib import admin
from django.contrib.admin import ModelAdmin

from weather.models import City


@admin.register(City)
class UserInfoAdminModel(ModelAdmin):
    pass
