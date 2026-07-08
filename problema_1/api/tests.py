from rest_framework.test import APITestCase
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


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
        logger.info("POST /dati-meteo/")
        logger.info("Request JSON: %s", data)

        response = self.client.post("/dati-meteo/", data, format="json")
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
        logger.info("POST /dati-meteo/")
        logger.info("Request JSON: %s", data)

        response = self.client.post("/dati-meteo/", data, format="json")

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
        logger.info("POST /dati-meteo/")
        logger.info("Request JSON: %s", data)

        response = self.client.post("/dati-meteo/", data, format="json")

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
        logger.info("POST /dati-meteo/")
        logger.info("Request JSON: %s", data)

        response = self.client.post("/dati-meteo/", data, format="json")
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
        logger.info("POST /dati-meteo/")
        logger.info("Request JSON: %s", data)

        response = self.client.post("/dati-meteo/", data, format="json")

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
        logger.info("POST /dati-meteo/")
        logger.info("Request JSON: %s", data)

        response = self.client.post("/dati-meteo/", data, format="json")

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
