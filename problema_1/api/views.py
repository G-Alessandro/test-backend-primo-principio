from rest_framework.decorators import api_view
from rest_framework.response import Response
import random
import operator


def crea_evento(bagnatura, humidity, temperature, rain):
    return (
        bagnatura == 1 and rain > 0
    ) or (
        bagnatura == 1 and humidity > 80 and temperature > 15
    )


def aggiorna_x(x):
    crescita = random.randrange(1, 10) / 10
    operazione = random.choice([operator.add, operator.mul])

    if x <= 0:
        operazione = operator.add

    if operazione == operator.mul:
        crescita += 1

    return min(1, round(operazione(x, crescita), 2))


@api_view(["POST"])
def dati_meteo(request):
    doy = request.data.get("doy")
    temperature = request.data.get("temperature")
    bagnatura = request.data.get("bagnatura")
    humidity = request.data.get("humidity")
    rain = request.data.get("rain")
    events = request.data.get("events", [])

    updated_events = []

    for event in events:
        updated_events.append({
            "index": event["index"],
            "X": aggiorna_x(event["X"])
        })

    if crea_evento(bagnatura, humidity, temperature, rain):
        if not updated_events:
            nuovo_index = 0
        else:
            ultimo_index = max(event["index"] for event in updated_events)
            nuovo_index = ultimo_index + 1

        updated_events.append({
            "index": nuovo_index,
            "X": 0.0
        })

    return Response({
        "doy": doy,
        "events": updated_events
    })
