#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup as soup
from BeautifulSoup import BeautifulSoup pas bs
import ssl
from urllib.request import Request, urlopen
from pprint import pprint







################ URL DON'T TOUCH ###############################
ssl._create_default_https_context = ssl._create_unverified_context
url_weather='https://weather.com/en-IN/weather/hourbyhour/l/75123f08c184dd588cecab22ff44d76291d59ce82122254dcb78b810b05b5253'
url_weather_news='https://www.meteoconsult.fr/actualites-meteo/dernieres-informations'
################ URL DON'T TOUCH ###############################
def main ():
	welcome_weather_script()
	weather()
	actus()

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
def weather():
	req = Request(url_weather, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	page_soup= soup(webpage, 'lxml')
	for item in page_soup.select('.clickable'):
		try:
			print(item)
			print(item.select('.day-detail')[0].get_text())
			print(item.select('.description')[0].get_text())
			print(item.select('.temp')[0].get_text())
			print(item.select('.precip')[0].get_text())
			print(item.select('.wind')[0].get_text())
			print(item.select('.humidity')[0].get_text())
			print('------------------')
			print('')
		except ValueError as error:	
			print(str(error))
			
def actus():
	req = Request(url_weather_news , headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	page_soup = soup(webpage, 'lxml')
	title = page_soup.find("title")
	subtitle = page_soup.find_all('h2')
	print("Votre actualité sur:\n\n ", title)
	print("Voici les sous-titres", subtitle)			

    
    

if __name__ == '__main__':
		main()	

		



	

