from rest_framework.decorators import api_view
from rest_framework.response import Response
import random
import operator


def crea_evento_v1(bagnatura, humidity, temperature, rain):
    return (
        bagnatura == 1 and rain > 0
    ) or (
        bagnatura == 1 and humidity > 80 and temperature > 15
    )


# Complessità Temporale: O(1)
def aggiorna_x(x):
    crescita = random.randrange(1, 10) / 10
    operazione = random.choice([operator.add, operator.mul])

    if x <= 0:
        operazione = operator.add

    if operazione == operator.mul:
        crescita += 1

    return min(1, round(operazione(x, crescita), 2))


@api_view(["POST"])
def dati_meteo_v1(request):
    doy = request.data.get("doy")
    temperature = request.data.get("temperature")
    bagnatura = request.data.get("bagnatura")
    humidity = request.data.get("humidity")
    rain = request.data.get("rain")
    events = request.data.get("events", [])

    eventi_aggiornati = []

    for evento in events:
        eventi_aggiornati.append({
            "index": evento["index"],
            "X": aggiorna_x(evento["X"])
        })

    if crea_evento_v1(bagnatura, humidity, temperature, rain):
        if not eventi_aggiornati:
            nuovo_index = 0
        else:
            ultimo_index = max(event["index"] for event in eventi_aggiornati)
            nuovo_index = ultimo_index + 1

        eventi_aggiornati.append({
            "index": nuovo_index,
            "X": 0.0
        })

    return Response({
        "doy": doy,
        "events": eventi_aggiornati
    })


# Complessità Temporale: O(m)
def crea_evento_v2(giorno, eventi_giorno, bagnatura, humidity, temperature, rain):
    # Verifica se le condizioni meteorologiche permettono la creazione
    # di un nuovo evento.
    condizioni_evento = ((bagnatura == 1 and rain > 0) or (
        bagnatura == 1 and humidity > 80 and temperature > 15))

    # Se le condizioni meteorologiche sono soddisfatte,
    # aggiunge un nuovo evento al giorno corrente.
    if condizioni_evento:

        # Se la struttura del giorno contiene già degli eventi,
        # recupera la relativa lista.
        if eventi_giorno:
            eventi = eventi_giorno["events"]

            # Se sono già presenti eventi, assegna al nuovo evento
            # un indice maggiore di uno rispetto all'indice più alto.
            if eventi:
                ultimo_index = max(evento["index"] for evento in eventi)
                nuovo_index = ultimo_index + 1

            # Se la lista degli eventi è vuota,
            # il primo evento riceve indice 0.
            else:
                nuovo_index = 0

            # Aggiunge il nuovo evento inizializzando X a 0.0
            eventi.append({
                "index": nuovo_index,
                "X": 0.0
            })

        # Se non esiste ancora una struttura per il giorno corrente,
        # la crea inserendo il primo evento con indice 0.
        else:
            eventi_giorno = {
                "doy": giorno["doy"], "events": [{"index": 0, "X": 0.0}]}

    # Se non si verificano le condizioni per creare un evento
    # e non esiste ancora una struttura per il giorno corrente,
    # crea il giorno con una lista di eventi vuota.
    elif not eventi_giorno:
        eventi_giorno = {"doy": giorno["doy"], "events": []}

    return eventi_giorno


# Complessità Temporale: O(n²)
# Complessità Spaziale: O(n²)
def gestisci_eventi(dati, giorno_precedente, lista_eventi):
    inizio_controllo = 0

    # Se il giorno precedente contiene eventi, li aggiunge a lista_eventi
    # e fa iniziare l'elaborazione dei dati dall'indice 1
    if "events" in giorno_precedente:
        inizio_controllo = 1
        lista_eventi.append({"doy": giorno_precedente["doy"],
                             "events": giorno_precedente["events"]})

    # farà un ciclo per ogni giorno al interno di data
    for i in range(inizio_controllo, len(dati)):
        giorno = dati[i]
        eventi_giorno_successivo = {}
        ultimo_giorno = None

        # Cerca, partendo dalla fine di lista_eventi,
        # il giorno più recente che contiene almeno un evento
        if lista_eventi:
            for giorno_eventi in reversed(lista_eventi):
                if giorno_eventi["events"]:
                    ultimo_giorno = giorno_eventi
                    break

        # Aggiorna il valore X degli eventi più recenti
        # e li associa al giorno attualmente elaborato
        if ultimo_giorno:
            ultimi_eventi_aggiornati = []

            for evento in ultimo_giorno["events"]:
                ultimi_eventi_aggiornati.append({
                    "index": evento["index"],
                    "X": aggiorna_x(evento["X"])
                })

            eventi_giorno_successivo = {
                "doy": giorno["doy"], "events": ultimi_eventi_aggiornati}

        # Verifica le condizioni meteorologiche del giorno corrente.
        # Se sono soddisfatte, aggiunge un nuovo evento alla lista
        # degli eventi già propagati dai giorni precedenti.
        #
        # Se non ci sono eventi precedenti e le condizioni non sono
        # soddisfatte, crea comunque la struttura del giorno
        # con una lista di eventi vuota.
        eventi_giorno_successivo = crea_evento_v2(
            giorno,
            eventi_giorno_successivo,
            giorno["bagnatura"],
            giorno["humidity"],
            giorno["temperature"],
            giorno["rain"]
        )

        # Salva nella lista il risultato relativo al giorno elaborato
        lista_eventi.append(eventi_giorno_successivo)


# Complessità Temporale: O(n²)
# Complessità Spaziale: O(n²)
@api_view(["POST"])
def dati_meteo_v2(request):
    giorno_precedente = request.data[0]
    giorni = []
    gestisci_eventi(request.data, giorno_precedente, giorni)

    return Response(giorni)
