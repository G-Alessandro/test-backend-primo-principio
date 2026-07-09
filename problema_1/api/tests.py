from rest_framework.test import APITestCase
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

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


class DatiMeteoApiTest(APITestCase):
    def test_crea_evento_quando_le_condizioni_sono_vere(self):
        data = {
            "doy": 126,
            "temperature": 15.94,
            "bagnatura": 1,
            "humidity": 97.25,
            "rain": 0.0

        }
        logger.info("=" * 50)
        logger.info("=== Inizio test: creazione evento ===")
        logger.info("=" * 50)
        logger.info("POST /dati-meteo/v1/")
        logger.info("Request JSON: %s", data)

        response = self.client.post("/dati-meteo/v1/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        logger.info("Status: %s", response.status_code)
        logger.info("Response JSON: %s", response.data)

        self.assertEqual(response.data["doy"], 126)
        self.assertEqual(len(response.data["events"]), 1)
        self.assertEqual(response.data["events"][0]["index"], 0)
        self.assertEqual(response.data["events"][0]["X"], 0.0)

        logger.info("Fine test")

    def test_nessun_evento_creato_quando_le_condizioni_sono_false(self):
        data = {
            "doy": 128,
            "temperature": 27.0,
            "bagnatura": 0,
            "humidity": 52.35,
            "rain": 0.0
        }

        logger.info("=" * 50)
        logger.info(
            "=== Inizio test: evento non creato con condizioni false ===")
        logger.info("=" * 50)
        logger.info("POST /dati-meteo/v1/")
        logger.info("Request JSON: %s", data)

        response = self.client.post("/dati-meteo/v1/", data, format="json")

        logger.info("Status: %s", response.status_code)
        logger.info("Response JSON: %s", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["events"], [])

        logger.info("Fine test")

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
        logger.info("=" * 50)
        logger.info("=== Inizio test: X non diminuisce ===")
        logger.info("=" * 50)
        logger.info("POST /dati-meteo/v1/")
        logger.info("Request JSON: %s", data)

        response = self.client.post("/dati-meteo/v1/", data, format="json")

        logger.info("Status: %s", response.status_code)
        logger.info("Response JSON: %s", response.data)

        old_x = data["events"][0]["X"]
        new_x = response.data["events"][0]["X"]
        self.assertGreaterEqual(new_x, old_x)

        logger.info("Fine test")

    def test_x_non_supera_uno(self):
        data = {
            "doy": 190,
            "temperature": 30.0,
            "bagnatura": 0,
            "humidity": 32.0,
            "rain": 0.0,
            "events": [
                {"index": 0, "X": 0.9}
            ]
        }

        logger.info("=" * 50)
        logger.info("=== Inizio test: X non supera uno ===")
        logger.info("=" * 50)
        logger.info("POST /dati-meteo/v1/")
        logger.info("Request JSON: %s", data)

        response = self.client.post("/dati-meteo/v1/", data, format="json")
        logger.info("Status: %s", response.status_code)
        logger.info("Response JSON: %s", response.data)

        self.assertLessEqual(response.data["events"][0]["X"], 1)
        logger.info("Fine test")

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
        logger.info("=" * 50)
        logger.info("=== Inizio test: nuovo evento viene aggiunto ===")
        logger.info("=" * 50)
        logger.info("POST /dati-meteo/v1/")
        logger.info("Request JSON: %s", data)

        response = self.client.post("/dati-meteo/v1/", data, format="json")

        logger.info("Status: %s", response.status_code)
        logger.info("Response JSON: %s", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["events"]), 2)
        self.assertEqual(response.data["events"][1]["index"], 1)
        self.assertEqual(response.data["events"][1]["X"], 0.0)

        logger.info("Fine test")

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
        logger.info("=" * 50)
        logger.info(
            "=== Inizio test: X aumenta in tutti gli eventi ===")
        logger.info("=" * 50)
        logger.info("POST /dati-meteo/v1/")
        logger.info("Request JSON: %s", data)

        response = self.client.post("/dati-meteo/v1/", data, format="json")

        logger.info("Status: %s", response.status_code)
        logger.info("Response JSON: %s", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["events"]), 3)

        self.assertEqual(response.data["events"][0]["index"], 0)
        self.assertGreaterEqual(response.data["events"][0]["X"], 0.9)
        self.assertLessEqual(response.data["events"][0]["X"], 1)

        self.assertEqual(response.data["events"][1]["index"], 1)
        self.assertGreaterEqual(response.data["events"][1]["X"], 0.3)
        self.assertLessEqual(response.data["events"][1]["X"], 1)

        self.assertEqual(response.data["events"][2]["index"], 2)
        self.assertGreaterEqual(response.data["events"][2]["X"], 0.6)
        self.assertLessEqual(response.data["events"][2]["X"], 1)

        logger.info("Fine test")


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
