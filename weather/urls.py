from django.urls import path

from weather import views
from weather.apps import WeatherConfig

app_name = WeatherConfig.label

urlpatterns = [
    path("", views.index),
]

