from django.urls import path

from apps.weather import views
from apps.weather.apps import WeatherConfig

app_name = WeatherConfig.label

urlpatterns = [
    path("", views.index, name="weather"),
]
