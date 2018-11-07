#!/usr/bin/env python

import json
import click
import requests

def get_json(queryParams):
    url = 'http://api.openweathermap.org/data/2.5/'

    if queryParams['weather']:
        url = url + 'weather'
    else:
        url = url + 'forecast'
    
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

def display_data(data):    
    click.secho('\t' + data['name'])
    click.secho('\tOpenWeather ID: {}'.format(data['id']))
    click.secho('\tTemperatura Actual: {}'.format(data['temp_actual']) + '°')
    click.secho('\tTemperatura Maxima: {}'.format(data['temp_max']) + '°', fg='red', bold=True)
    click.secho('\tTemperatura Minima: {}'.format(data['temp_min']) + '°', fg='cyan', bold=True)    
    
@click.command()
@click.option('--city', '-c', default="", help='Name of the City')
@click.option('--id', '-i', default="", help='OpenWeather ID of the City ')
@click.option('--api-key', '-a', default="", help='OpenWeather API Key')
@click.option('--lang', '-l', default="es", help='Set request lenguage')
@click.option('--units', '-u', default='metric', help='Unit format. The default format is metric',
type=click.Choice(['metric', 'imperial']))
@click.option('--weather', 'time', default=True,  help='Get current weather. Default option')
@click.option('--forecast', 'time', default=False, help='Get forecast of the city. Current daily')
def main(city, id, api_key, lang, units, time):

    if api_key is not "":
        apikey = api_key

    query_params = {
		'appid': apikey,
		'lang': lang,
        'units': units,
        'weather': 'false'
        'forecast': 'false'
    }

    if time:
        query_params['weather'] = 'true'
    else:
        query_params['forecast'] = 'true'
   
    if city is "":
        query_params['id'] = id
    else:
        query_params['q'] = city
        
    data = get_json(query_params)
    display_data(data)

if __name__ == "__main__":
	main()