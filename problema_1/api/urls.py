from django.urls import path
from .views import dati_meteo_v1, dati_meteo_v2

urlpatterns = [
    path("dati-meteo/v1/", dati_meteo_v1),
    path("dati-meteo/v2/", dati_meteo_v2),
]
