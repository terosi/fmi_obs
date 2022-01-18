import requests
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup

class Observation:
    temperature = None
    wind_speed = None
    wind_gust = None
    wind_direction = None
    relative_humidity = None
    dew_point = None
    precipitation_amount = None
    precipitation_intensity = None
    snow_depth = None
    air_pressure = None
    horizontal_visibility = None
    cloud_amount = None
    present_weather = None


def get_observation(place: str):
    """
    Get latest weather observation
    place: Location (e.g. Helsinki)
    return: Weather observation class
    """
    end_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    start_time = end_time - timedelta(minutes=11)
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "getFeature",
        "storedquery_id": "fmi::observations::weather::multipointcoverage",
        "timestep": 10,
        "starttime": start_time.isoformat(timespec="seconds"),
        "endtime": end_time.isoformat(timespec="seconds"),
    }

    if place is not None:
        params["place"] = place.strip().replace(" ", "")

    url = "http://opendata.fmi.fi/wfs"

    try:
        r = requests.get(url, params=params)
    except Exception as e:
        raise e

    try:
        soup = BeautifulSoup(r.content, "lxml")
        samples = soup.find("gml:doubleornilreasontuplelist").get_text().strip()
        s_list = samples.split(" ")
        if len(s_list) < 13:
            raise Exception
        obs = Observation
        obs.temperature = s_list[0]
        obs.wind_speed = s_list[1]
        obs.wind_gust = s_list[2]
        obs.wind_direction = s_list[3]
        obs.relative_humidity = s_list[4]
        obs.dew_point = s_list[5]
        obs.precipitation_amount = s_list[6]
        obs.precipitation_intensity = s_list[7]
        obs.snow_depth = s_list[8]
        obs.air_pressure = s_list[9]
        obs.horizontal_visibility = s_list[10]
        obs.cloud_amount = s_list[11]
        obs.present_weather = s_list[12]
        return obs
    except Exception as e:
        raise e


def main():
    try:
        obs = get_observation("Pirkkala")
        print(obs.temperature)
    except Exception as e:
        print("Error obtaining weather observation.")


if __name__ == "__main__":
    main()
