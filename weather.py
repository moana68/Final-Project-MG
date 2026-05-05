# weather.py
import requests

def get_current_weather(city="Tirana"):
    # First get coordinates for the city
    geo = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    ).json()

    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]

    # Then get current temperature
    weather = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    ).json()

    temp = weather["current_weather"]["temperature"]

    # Map temperature to your categories
    if temp < 10:
        return "cold"
    elif temp < 22:
        return "warm"
    else:
        return "any"
