import requests
from django.contrib.gis import geoip2
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.template.defaultfilters import safe

from weather.forms import CityForm
from weather.models import City

appid = "b4be221bb02fa8a7be1d57407c585b5b"
url = "http://api.openweathermap.org/data/2.5/find?q={}&units=metric&appid=" + appid


def index(request):
    err_msg = ""
    message = ""
    message_class = ""

    if request.method == "POST":
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data["name"]
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                res = requests.get(url.format(new_city)).json()
                if res["cod"] == "200":
                    form.save()
                else:
                    err_msg = "Такого города не существует"
                    # сюда надо что-то, чтоб удалялась ячейка с херней-городом из базы данных
            else:
                err_msg = "Погода для этого города уже отображена"
        if err_msg:
            message = err_msg
            message_class = "is-danger"
        else:
            message = "Город успешно добавлен"
            message_class = "is-sucess"

    form = CityForm()

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            "city": city.name,
            "temp": res["list"][0]["main"]["temp"],
            "icon": res["list"][0]["weather"][0]["icon"],
        }

        all_cities.append(city_info)

    context = {
        "all_info": all_cities,
        "form": form,
        "message": message,
        "message_class": message_class,
    }

    return render(request, "weather/index.html", context)


def get_real_ip(request: HttpRequest):
    reader = geoip2.database.Reader("src/GeoLite2-City.mmdb")
    city = retrieve_ip()
    if city is not None:
        response = reader.city(city)
        return response
    response = reader.city("178.120.37.5")
    all_cities_ip = []
    r = requests.get(url.format(response)).json()
    city_info_ip = {
        "city": response,
        "temp": r["list"][0]["main"]["temp"],
        "icon": r["list"][0]["weather"][0]["icon"],
    }
    all_cities_ip.append(city_info_ip)
    context = {"all_cities_ip": all_cities_ip}
    return render(request, "weather/index.html", context)


@safe
def retrieve_ip(ip: str):
    resp = requests.get(f"http://ip-api.com/json/{ip}")
    payload = resp.json()
    city = payload.get("city")
    if resp.status_code != 200:
        return None
    else:
        return city

def delete_city(request, city_name):
    assert request
    city = City.objects.get(name=city_name)
    city.delete()
    return redirect('home')
