import os
import time
import requests
from datetime import datetime

# Icônes ASCII météo
WEATHER_ICONS = {
    "clear": "☀️",
    "mainly_clear": "🌤️",
    "partly_cloudy": "⛅",
    "overcast": "☁️",
    "fog": "🌫️",
    "drizzle": "🌦️",
    "rain": "🌧️",
    "snow": "❄️",
    "thunderstorm": "⛈️",
    "unknown": "❓"
}

# Codes Open-Meteo → description + icône
def get_condition_info(code):
    mapping = {
        0: ("Ensoleillé", "clear"),
        1: ("Principalement clair", "mainly_clear"),
        2: ("Partiellement nuageux", "partly_cloudy"),
        3: ("Couvert", "overcast"),
        45: ("Brouillard", "fog"),
        48: ("Brouillard givrant", "fog"),
        51: ("Bruine légère", "drizzle"),
        53: ("Bruine modérée", "drizzle"),
        55: ("Bruine dense", "drizzle"),
        61: ("Pluie légère", "rain"),
        63: ("Pluie modérée", "rain"),
        65: ("Forte pluie", "rain"),
        71: ("Neige légère", "snow"),
        73: ("Neige modérée", "snow"),
        75: ("Forte neige", "snow"),
        95: ("Orage", "thunderstorm"),
        99: ("Orage violent", "thunderstorm"),
    }
    label, icon_key = mapping.get(code, ("Inconnu", "unknown"))
    return label, WEATHER_ICONS.get(icon_key, "❓")

# Rechercher les coordonnées d’une ville via Nominatim
def get_coordinates(city_name):
    url = f"https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "weather-terminal-app"
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        results = response.json()
        if results:
            lat = float(results[0]["lat"])
            lon = float(results[0]["lon"])
            return lat, lon
        else:
            print("Ville introuvable.")
            return None
    except Exception as e:
        print(f"Erreur lors de la géolocalisation : {e}")
        return None

# Appel à l’API météo
def fetch_weather(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&daily=temperature_2m_min,temperature_2m_max,weathercode,precipitation_sum,windspeed_10m_max"
        "&timezone=auto"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        days = []

        for i in range(7):
            date_str = data["daily"]["time"][i]
            day = datetime.strptime(date_str, "%Y-%m-%d").strftime("%A %d %b")
            temp_min = data["daily"]["temperature_2m_min"][i]
            temp_max = data["daily"]["temperature_2m_max"][i]
            wind = data["daily"]["windspeed_10m_max"][i]
            rain = data["daily"]["precipitation_sum"][i]
            code = data["daily"]["weathercode"][i]
            condition_text, icon = get_condition_info(code)

            days.append({
                "day": day,
                "condition": condition_text,
                "icon": icon,
                "temp_min": temp_min,
                "temp_max": temp_max,
                "rain": rain,
                "wind": wind
            })

        return days

    except requests.RequestException as e:
        print(f"Erreur API météo : {e}")
        return []

# Affiche les prévisions
def display_weather(city, data):
    print("\033[1;34m" + "="*55)
    print(f"   MÉTÉO À {city.upper()} - PROCHAINS 7 JOURS")
    print("="*55 + "\033[0m")

    for day in data:
        print(f"\n\033[1;33m{day['day']}\033[0m")
        print(f"  Condition : {day['icon']}  {day['condition']}")
        print(f"  Températures : {day['temp_min']}°C - {day['temp_max']}°C")
        print(f"  Pluie : {day['rain']} mm")
        print(f"  Vent : {day['wind']} km/h")

    print("\n\033[2mDernière mise à jour : " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\033[0m")

# Boucle principale
def main_loop(city):
    coords = get_coordinates(city)
    if not coords:
        return
    lat, lon = coords
    try:
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            weather = fetch_weather(lat, lon)
            if weather:
                display_weather(city, weather)
            else:
                print("Erreur de récupération météo.")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n\033[91mArrêt du programme météo.\033[0m")

# Point d’entrée
if __name__ == "__main__":
    ville = input("Entrez le nom d'une ville : ")
    main_loop(ville.strip())
