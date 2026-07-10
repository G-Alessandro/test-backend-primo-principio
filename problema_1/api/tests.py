from rest_framework.test import APITestCase
from rest_framework import status

# dati con il primo giorno contenente l'evento che verra propagato e incrementato nei giorni successivi
data_test_1_v2 = [{"doy": 189, "temperature": 28.9, "bagnatura": 0, "humidity": 43, "rain": 0.2,
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

# dati senza eventi con il primo e terzo giorno idonei al ricevimento
data_test_2_v2 = [{"doy": 189, "temperature": 28.9,
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

# dati senza eventi con solo il terzo giorno idoneo al ricevimento del evento
data_test_3_v2 = [{"doy": 189, "temperature": 28.9, "bagnatura": 0, "humidity": 43, "rain": 0.0},
                  {"doy": 190, "temperature": 28.4,
                   "bagnatura": 0, "humidity": 58, "rain": 0.0},
                  {"doy": 191, "temperature": 28.3,
                   "bagnatura": 1, "humidity": 50, "rain": 1.2},
                  {"doy": 192, "temperature": 26.7,
                   "bagnatura": 0, "humidity": 68, "rain": 0.0},
                  {"doy": 193, "temperature": 28.6,
                   "bagnatura": 0, "humidity": 63, "rain": 0.0},
                  {"doy": 194, "temperature": 29.3,
                   "bagnatura": 0, "humidity": 61, "rain": 0.0},
                  {"doy": 195, "temperature": 29.3, "bagnatura": 0, "humidity": 59, "rain": 0.0}]


class DatiMeteoV1ApiTest(APITestCase):
    def test_crea_evento_quando_le_condizioni_sono_vere(self):
        data = {
            "doy": 126,
            "temperature": 15.94,
            "bagnatura": 1,
            "humidity": 97.25,
            "rain": 0.0
        }

        response = self.client.post("/dati-meteo/v1/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("events", response.data)
        self.assertEqual(response.data["doy"], 126)

        eventi = response.data["events"]
        self.assertEqual(len(eventi), 1)
        evento = eventi[0]
        self.assertEqual(evento["index"], 0)
        self.assertEqual(evento["X"], 0.0)

    def test_nessun_evento_creato_quando_le_condizioni_sono_false(self):
        data = {
            "doy": 128,
            "temperature": 27.0,
            "bagnatura": 0,
            "humidity": 52.35,
            "rain": 0.0
        }

        response = self.client.post("/dati-meteo/v1/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("events", response.data)
        self.assertEqual(response.data["doy"], 128)

        eventi = response.data["events"]
        self.assertEqual(len(eventi), 0)

    def test_x_non_diminuisce(self):
        data = {
            "doy": 127,
            "temperature": 17.15,
            "bagnatura": 1,
            "humidity": 42.35,
            "rain": 0.0,
            "events": [
                {"index": 0, "X": 0.2}
            ]
        }

        response = self.client.post("/dati-meteo/v1/", data, format="json")

        self.assertIn("events", response.data)
        self.assertEqual(response.data["doy"], 127)

        eventi = response.data["events"]
        self.assertEqual(len(eventi), 1)

        evento = eventi[0]
        self.assertEqual(evento["index"], 0)

        x_precedente = data["events"][0]["X"]
        x_incrementato = evento["X"]
        self.assertGreaterEqual(x_incrementato, x_precedente)

    def test_x_non_supera_uno(self):
        data = {
            "doy": 190,
            "temperature": 30.0,
            "bagnatura": 0,
            "humidity": 32.0,
            "rain": 0.0,
            "events": [
                {"index": 0, "X": 1.0}
            ]
        }

        response = self.client.post("/dati-meteo/v1/", data, format="json")

        self.assertIn("events", response.data)
        self.assertEqual(response.data["doy"], 190)

        eventi = response.data["events"]
        self.assertEqual(len(eventi), 1)
        evento = eventi[0]
        self.assertEqual(evento["index"], 0)
        self.assertLessEqual(evento["X"], 1)

    def test_nuovo_evento_viene_aggiunto(self):
        data = {
            "doy": 129,
            "temperature": 37.0,
            "bagnatura": 1,
            "humidity": 42.35,
            "rain": 10.0,
            "events": [
                {"index": 0, "X": 0.4}
            ]
        }

        response = self.client.post("/dati-meteo/v1/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("events", response.data)
        self.assertEqual(response.data["doy"], 129)

        eventi = response.data["events"]
        self.assertEqual(len(eventi), 2)

        evento_esistente, nuovo_evento = eventi
        self.assertEqual(evento_esistente["index"], 0)
        self.assertGreater(evento_esistente["X"], 0.4)
        self.assertEqual(nuovo_evento["index"], 1)
        self.assertEqual(nuovo_evento["X"], 0.0)

    def test_x_in_tutti_gli_eventi_aumenta(self):
        data = {
            "doy": 128,
            "temperature": 27.0,
            "bagnatura": 0,
            "humidity": 52.35,
            "rain": 0.0,
            "events": [
                {"index": 0, "X": 0.9},
                {"index": 1, "X": 0.3},
                {"index": 2, "X": 0.6}
            ]
        }

        response = self.client.post("/dati-meteo/v1/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("events", response.data)
        self.assertEqual(response.data["doy"], 128)

        eventi = response.data["events"]
        self.assertEqual(len(eventi), 3)

        for i, evento in enumerate(eventi):
            self.assertEqual(evento["index"], i)
            self.assertGreater(evento["X"], data["events"][i]["X"])
            print(evento["index"], i, evento["X"], data["events"][i]["X"])


class DatiMeteoV2ApiTest(APITestCase):
    # il primo giorno contiene due eventi che devono essere aggiunti e incrementati nei giorni successivi
    def test_propagazione_evento_con_incremento_di_x(self):
        data = data_test_1_v2
        response = self.client.post("/dati-meteo/v2/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        x_precedente_index_zero = next(
            evento["X"] for evento in response.data[0]["events"] if evento["index"] == 0
        )

        x_precedente_index_uno = next(
            evento["X"] for evento in response.data[0]["events"] if evento["index"] == 1
        )

        for giorno in response.data[1:]:
            self.assertIn("events", giorno)
            self.assertEqual(len(giorno["events"]), 2)

            evento_index_uno = next(
                evento for evento in giorno["events"] if evento["index"] == 1
            )
            evento_index_zero = next(
                evento for evento in giorno["events"] if evento["index"] == 0
            )

            self.assertGreaterEqual(
                evento_index_zero["X"],
                x_precedente_index_zero
            )
            self.assertGreaterEqual(
                evento_index_uno["X"],
                x_precedente_index_uno
            )

            x_precedente_index_zero = evento_index_zero["X"]
            x_precedente_index_uno = evento_index_uno["X"]

    # viene aggiunto un evento al primo e terzo giorno incrementandoli nei giorni successivi
    def test_aggiunta_evento_al_primo_e_terzo_giorno(self):
        data = data_test_2_v2
        response = self.client.post("/dati-meteo/v2/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        x_precedente_index_zero = next(
            evento["X"] for evento in response.data[0]["events"] if evento["index"] == 0
        )

        x_precedente_index_uno = next(
            evento["X"] for evento in response.data[2]["events"] if evento["index"] == 1
        )

        for i, giorno in enumerate(response.data):
            self.assertIn("events", giorno)

            if i < 2:
                self.assertEqual(len(giorno["events"]), 1)
            else:
                self.assertEqual(len(giorno["events"]), 2)

                evento_index_uno = next(
                    evento for evento in giorno["events"] if evento["index"] == 1
                )

                self.assertGreaterEqual(
                    evento_index_uno["X"],
                    x_precedente_index_uno
                )

                x_precedente_index_uno = evento_index_uno["X"]

            evento_index_zero = next(
                evento for evento in giorno["events"] if evento["index"] == 0
            )

            self.assertGreaterEqual(
                evento_index_zero["X"],
                x_precedente_index_zero
            )

            x_precedente_index_zero = evento_index_zero["X"]

    # il primo evento viene aggiunto al terzo giorno per poi incrementarlo nei giorni successivi
    def test_aggiunta_evento_a_partire_dal_terzo_giorno(self):
        data = data_test_3_v2
        response = self.client.post("/dati-meteo/v2/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        x_precedente_index_zero = next(
            evento["X"] for evento in response.data[2]["events"] if evento["index"] == 0
        )

        for i, giorno in enumerate(response.data):
            self.assertIn("events", giorno)

            if i < 2:
                self.assertEqual(len(giorno["events"]), 0)
            else:
                self.assertEqual(len(giorno["events"]), 1)

                evento_index_zero = next(
                    evento for evento in giorno["events"] if evento["index"] == 0
                )

                self.assertGreaterEqual(
                    evento_index_zero["X"],
                    x_precedente_index_zero
                )

                x_precedente_index_zero = evento_index_zero["X"]
