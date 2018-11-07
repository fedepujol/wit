#!/usr/bin/env python3

import json
import click
import requests

def get_json(queryParams):
    url = 'http://api.openweathermap.org/data/2.5/weather'
    res = requests.get(url, params=queryParams)

    dt = res.json()

    data = {
        'id': dt['id'],
        'name': dt['name'],
        'temp_actual': dt['main']['temp'],
        'temp_max': dt['main']['temp_max'],
        'temp_min': dt['main']['temp_min'],
        'desc': dt['weather'][0]['description']
    }

    return data

@click.command()
@click.option('--city', '-c', default="", help='Name of the City')
@click.option('--id', '-i', default="", help='OpenWeather ID of the City ')
@click.option('--api-key', '-a', default="", help='OpenWeather API Key')
@click.option('--lang', '-l', default="es", help='Set request lenguage')
@click.option('--units', '-u', default='metric', help='Unit format. The default format is metric',
type=click.Choice(['metric', 'imperial']))
def main(city, id, api_key, lang, units):
	

	if api_key is not "":
		apikey = api_key

	query_params = {
		'appid': apikey,
		'lang': lang,
        'units': units
	}	
	
	if city is "":
		query_params['id'] = id
	else:
		query_params['q'] = city

	print(get_json(query_params))

if __name__ == "__main__":
	main()