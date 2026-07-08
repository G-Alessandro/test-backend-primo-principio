from django.urls import path

from .views import dati_meteo
urlpatterns = [
    path("dati-meteo/", dati_meteo),
]