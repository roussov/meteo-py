#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import ssl
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from pprint import pprint
import os
from pushbullet import Pushbullet
import json, urllib

PB_API_KEY = ""
OWM_API_KEY = "" # Votre API Open Weather Map
NOTIF_TITLE = "Météo du jour"
DEVICE_ID = ""; # Send to specific device (run print(pb.devices) to get key)
OWM_API_BASE_URL = "http://api.openweathermap.org/data/2.5/"






################ URL DON'T TOUCH ###############################
ssl._create_default_https_context = ssl._create_unverified_context
url_weather_news='https://www.meteoconsult.fr/actualites-meteo/dernieres-informations'
################ URL DON'T TOUCH ###############################
def main ():
	welcome_weather_script()
	getWeather()
	actus()
	os.system("PAUSE")
	


def welcome_weather_script():
	daddy_go_welcome = """

                                                                                  
  _____            _     _               _____  ____  
 |  __ \          | |   | |             / ____|/ __ \ 
 | |  | | __ _  __| | __| |_   _ ______| |  __| |  | |
 | |  | |/ _` |/ _` |/ _` | | | |______| | |_ | |  | |
 | |__| | (_| | (_| | (_| | |_| |      | |__| | |__| |
 |_____/ \__,_|\__,_|\__,_|\__, |       \_____|\____/ 
                            __/ |                     
                           |___/                      

  __  __      _             
 |  \/  |    | |            
 | \  / | ___| |_ ___  ___  
 | |\/| |/ _ \ __/ _ \/ _ \ 
 | |  | |  __/ ||  __/ (_) |
 |_|  |_|\___|\__\___|\___/ 
 
 \n\n
"""
	print(daddy_go_welcome)

			
def actus():

	req = Request(url_weather_news , headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	page_soup = soup(webpage, "html.parser")
	title = page_soup.find("title")
	subtitle = page_soup.find_all('h2')
	print("Votre actualité sur:\n\n ", title)
	print("Voici les sous-titres", subtitle)
				

    
def getWeather():
	content = ""
	CITY = input("Indiquez votre ville -> \n")
	weather_gps = json.loads(urllib.request.urlopen(OWM_API_BASE_URL+"weather?APPID="+OWM_API_KEY+"&q="+urllib.parse.quote_plus(CITY.encode("utf8"))+"&mode=json&units=metric").read())
	if 'lon' in weather_gps['coord']:
		gps_lon = str(weather_gps['coord']['lon'])
		gps_lat = str(weather_gps['coord']['lat'])
		weather = json.loads(urllib.request.urlopen(OWM_API_BASE_URL+"onecall?APPID="+OWM_API_KEY+"&lat="+gps_lat+"&lon="+gps_lon+"&units=metric&lang=fr&exclude=hourly").read())
		if 'current' in weather:
			current_temp = str(weather['current']['temp'])
			current_temp_feels = str(weather['current']['feels_like'])
			weather_desc = str(weather['current']['weather'][0]['description'])
			day_max_temp =  str(weather['daily'][0]['temp']['max'])
			content = "Il fait actuellement "+current_temp+"°C ("+current_temp_feels+"°C ressenti) à "+CITY+"."
			content += "\n"
			content += "Le temps est "+weather_desc+"."
			content += "\n"
			content += "La maximale sera de "+day_max_temp+"°C."
			print(content);  

if __name__ == '__main__':
		main()	

			
	
