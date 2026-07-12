from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services.open_meteo import recupera_dati_meteo
import requests
from .models import StoricoEventi
from django.conf import settings

@api_view(["POST"])
def registra_eventi(request):

    try:
        dati_meteo = recupera_dati_meteo(
            latitude=settings.LATITUDINE_OPEN_METEO,
            longitude=settings.LONGITUDINE_OPEN_METEO
        )
        response = requests.post(
            f"{settings.PROBLEMA_1_BASE_URL}/dati-meteo/v2/",
            json=dati_meteo,
            timeout=30
        )
        response.raise_for_status()

    except requests.RequestException as exc:
        return Response(
            {
                "messaggio": "Errore durante la chiamata al Problema 1",
                "errore": str(exc),
            },
            status=status.HTTP_502_BAD_GATEWAY,
        )

    eventi_oidio = response.json()

    eventi_da_salvare = [
        StoricoEventi(
            doy=giorno["doy"],
            event_index=evento["index"],
            x_value=evento["X"],
        )
        for giorno in eventi_oidio
        for evento in giorno.get("events", [])
    ]

    with transaction.atomic():
        StoricoEventi.objects.bulk_create(
            eventi_da_salvare, ignore_conflicts=True)

    return Response({
        "messaggio": "Eventi salvati correttamente",
        "eventi_oidio": eventi_oidio,
        "dati_meteo": dati_meteo
    }, status=status.HTTP_201_CREATED)
