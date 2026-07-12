from datetime import date, timedelta, datetime
import requests
from django.conf import settings


def formatta_dati_meteo(weather_data):
    daily = weather_data["daily"]
    result = []

    for i, date_str in enumerate(daily["time"]):
        dt = datetime.strptime(date_str, "%Y-%m-%d")

        temperature = round(daily["temperature_2m_mean"][i], 1)
        humidity = round(daily["relative_humidity_2m_mean"][i], 1)
        rain = round(daily["precipitation_sum"][i], 1)

        bagnatura = int(rain >= 0.2 or (
            humidity >= 85 and temperature <= 20))

        result.append({
            "doy": dt.timetuple().tm_yday,
            "date": dt.strftime("%d/%m/%Y"),
            "temperature": temperature,
            "bagnatura": bagnatura,
            "humidity": humidity,
            "rain": rain,
        })

    return result


def recupera_dati_meteo(latitude, longitude):
    today = date.today()

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": (today - timedelta(days=1)).isoformat(),
        "end_date": (today + timedelta(days=6)).isoformat(),
        "daily": ",".join([
            "temperature_2m_mean",
            "relative_humidity_2m_mean",
            "precipitation_sum",
        ]),
        "timezone": "auto"
    }

    response = requests.get(settings.OPEN_METEO_URL, params=params,
                            timeout=30)

    response.raise_for_status()

    return formatta_dati_meteo(response.json())
