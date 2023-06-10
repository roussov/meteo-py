#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
from datetime import datetime, timedelta

# Entrez votre clé API OpenWeatherMap ci-dessous
api_key = "votre clé API"

# Entrez votre nom de ville ci-dessous
ville = "votre ville"

# Récupérer les prévisions météo pour les sept prochains jours
url = f"http://api.openweathermap.org/data/2.5/forecast?q={ville}&units=metric&appid={api_key}"
response = requests.get(url)

# Afficher les prévisions météo pour chaque jour
data = response.json()
for prevision in data["list"]:
    date = datetime.fromtimestamp(int(prevision["dt"])).strftime("%Y-%m-%d")
    jour = datetime.fromtimestamp(int(prevision["dt"])).strftime("%A")
    temps = prevision["weather"][0]["description"]
    temperature = prevision["main"]["temp"]
    print(f"{jour} ({date}): {temps} - {temperature}°C")
