from django.forms import ModelForm
from django.forms import TextInput

from apps.weather.models import City


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ["name"]
        widjets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "name": "city",
                    "id": "city",
                    "placeholder": "Введите город",
                }
            )
        }
