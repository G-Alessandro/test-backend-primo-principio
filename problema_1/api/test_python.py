import operator
import random
from pprint import pprint

# dati con il primo dizionario che non contiene un evento e non soddisfa i requisiti per riceverlo
data = [{"doy": 189, "temperature": 28.9, "bagnatura": 0, "humidity": 43, "rain": 0.0},
        {"doy": 190, "temperature": 28.4, "bagnatura": 0, "humidity": 58, "rain": 0.0},
        {"doy": 191, "temperature": 28.3, "bagnatura": 0, "humidity": 50, "rain": 0.0},
        {"doy": 192, "temperature": 26.7, "bagnatura": 1, "humidity": 68, "rain": 2.6},
        {"doy": 193, "temperature": 28.6, "bagnatura": 0, "humidity": 63, "rain": 0.0},
        {"doy": 194, "temperature": 29.3, "bagnatura": 0, "humidity": 61, "rain": 0.0},
        {"doy": 195, "temperature": 29.3, "bagnatura": 0, "humidity": 59, "rain": 0.0}]

# dati con il primo dizionario che non contiene un evento ma soddisfa i requisiti per riceverlo
data2 = [{"doy": 189, "temperature": 28.9, "bagnatura": 0, "humidity": 43, "rain": 0.0},
         {"doy": 190, "temperature": 28.4,
             "bagnatura": 0, "humidity": 58, "rain": 0.0},
         {"doy": 191, "temperature": 28.3,
             "bagnatura": 0, "humidity": 50, "rain": 0.0},
         {"doy": 192, "temperature": 26.7,
             "bagnatura": 1, "humidity": 68, "rain": 2.6},
         {"doy": 193, "temperature": 28.6,
             "bagnatura": 0, "humidity": 63, "rain": 0.0},
         {"doy": 194, "temperature": 29.3,
             "bagnatura": 0, "humidity": 61, "rain": 0.0},
         {"doy": 195, "temperature": 29.3, "bagnatura": 0, "humidity": 59, "rain": 0.0}]

# dati con il primo dizionario che contiene un evento e non vero per riceverlo
data3 = [{"doy": 189, "temperature": 28.9, "bagnatura": 1, "humidity": 43, "rain": 0.2,
         "events": [{"index": 0, "X": 0.7}, {"index": 1, "X": 0.0}]},
         {"doy": 190, "temperature": 28.4,
             "bagnatura": 0, "humidity": 58, "rain": 0.0},
         {"doy": 191, "temperature": 28.3,
             "bagnatura": 0, "humidity": 50, "rain": 0.0},
         {"doy": 192, "temperature": 26.7,
             "bagnatura": 1, "humidity": 68, "rain": 2.6},
         {"doy": 193, "temperature": 28.6,
             "bagnatura": 0, "humidity": 63, "rain": 0.0},
         {"doy": 194, "temperature": 29.3,
             "bagnatura": 0, "humidity": 61, "rain": 0.0},
         {"doy": 195, "temperature": 29.3, "bagnatura": 0, "humidity": 59, "rain": 0.0}]

data_test_1 = [{"doy": 189, "temperature": 28.9, "bagnatura": 0, "humidity": 43, "rain": 0.2,
                "events": [{"index": 0, "X": 0.7}, {"index": 1, "X": 0.0}]},
               {"doy": 190, "temperature": 28.4,
                "bagnatura": 0, "humidity": 58, "rain": 0.0},
               {"doy": 191, "temperature": 28.3,
                "bagnatura": 0, "humidity": 50, "rain": 0.0},
               {"doy": 192, "temperature": 26.7,
                "bagnatura": 1, "humidity": 68, "rain": 0.0},
               {"doy": 193, "temperature": 28.6,
                "bagnatura": 0, "humidity": 63, "rain": 0.0},
               {"doy": 194, "temperature": 29.3,
                "bagnatura": 0, "humidity": 61, "rain": 0.0},
               {"doy": 195, "temperature": 29.3, "bagnatura": 0, "humidity": 59, "rain": 0.0}]

data_test_2 = [{"doy": 189, "temperature": 28.9,
                "bagnatura": 1, "humidity": 43, "rain": 0.9},
               {"doy": 190, "temperature": 28.4,
                "bagnatura": 0, "humidity": 58, "rain": 0.0},
               {"doy": 191, "temperature": 28.3,
                "bagnatura": 1, "humidity": 50, "rain": 1.0},
               {"doy": 192, "temperature": 26.7,
                "bagnatura": 0, "humidity": 68, "rain": 2.6},
               {"doy": 193, "temperature": 28.6,
                "bagnatura": 0, "humidity": 63, "rain": 0.0},
               {"doy": 194, "temperature": 29.3,
                "bagnatura": 0, "humidity": 61, "rain": 0.0},
               {"doy": 195, "temperature": 29.3, "bagnatura": 0, "humidity": 59, "rain": 0.0}]


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


def dati_meteo(request):
    giorno_precedente = request[0]
    inizio_controllo = 0
    eventi = []
    # controlla se ci sono eventi al interno del giorno precedente(ieri)
    if "events" in giorno_precedente:
        inizio_controllo = 1
        eventi.append({"doy": giorno_precedente["doy"],
                      "events": giorno_precedente["events"]})

    for i in range(inizio_controllo, len(request)):
        giorno = request[i]
        eventi_giorno_successivo = []
        ultimo_evento = None

        # aggiorna gli eventi dei giorni precedenti

        if eventi:
            for giorno_eventi in reversed(eventi):
                if giorno_eventi["events"]:
                    ultimo_evento = giorno_eventi
                    break

        if ultimo_evento:
            ultimi_eventi_aggiornati = []

            for evento in ultimo_evento["events"]:
                ultimi_eventi_aggiornati.append({
                    "index": evento["index"],
                    "X": aggiorna_x(evento["X"])
                })

            eventi_giorno_successivo.append(
                {"doy": giorno["doy"], "events": ultimi_eventi_aggiornati})

        # Crea un nuovo evento se le condizioni lo permettono
        if crea_evento(giorno["bagnatura"], giorno["humidity"], giorno["temperature"], giorno["rain"]):

            if eventi_giorno_successivo:
                ultimo_index = max(evento["index"]
                                   for evento in eventi_giorno_successivo[0]["events"])
                nuovo_index = ultimo_index + 1

                eventi_giorno_successivo[0]["events"].append({
                    "index": nuovo_index,
                    "X": 0.0
                })
            else:
                eventi_giorno_successivo.append({
                    "doy": giorno["doy"], "events": [{"index": 0, "X": 0.0}]
                })
        elif not eventi_giorno_successivo:
            eventi_giorno_successivo.append({
                "doy": giorno["doy"], "events": []
            })

        for evento in eventi_giorno_successivo:
            eventi.append(evento)

    return eventi


# risultato_test = dati_meteo(data_test_2)
# pprint(risultato_test, sort_dicts=False)
