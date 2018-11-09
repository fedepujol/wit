#!/usr/bin/env python3

import json
import click
import requests
import geocoder

def get_json(queryParams):
    url = 'http://api.openweathermap.org/data/2.5/weather'
   
    res = requests.get(url, params=queryParams)
    dt = res.json()

    data = {
        'name': dt['name'],
        'id': dt['id'],
        'temp_actual': dt['main']['temp'],
        'desc': dt['weather'][0]['description'],
        'viento': dt['wind']['speed']
    }

    return data

def display_data(data):
    click.secho('\t' + data['name'])
    click.secho('\tOpenWeather ID: {}'.format(data['id']))
    format_temp_actual(data['temp_actual'])
    click.secho('\tClima actual: {}'.format(data['desc']))
    click.secho('\tVel. Viento: {}'.format(data['viento']))

def format_temp_actual(temp):
    if temp > 25:
        display_temp_actual(temp, 'red')
    elif temp > 15 and temp <= 25:
        display_temp_actual(temp, 'yellow')
    elif temp <= 15:
        display_temp_actual(temp, 'cyan')

def display_temp_actual(temp, color):
    click.secho('\tTemperatura Actual: {}'.format(temp) + '°', fg=color, bold=True)

def get_geo_coords(queryParams):
    coords = geocoder.ip('me')
    lat = coords.latlng[0]
    lng = coords.latlng[1]

    queryParams = set_query_param(queryParams, 'lat', lat)
    queryParams = set_query_param(queryParams, 'lon', lng)

    return queryParams

def set_query_param(query, attr, param):
    query[attr] = param
    return query

def query_builder(city, id, api_key, lang, units, cnt_loc):
    query_params = {
		'appid': api_key,
		'lang': lang,
        'units': units
    }

    if cnt_loc:
        query_params = get_geo_coords(query_params)
    else:
        if city is "":
            query_params = set_query_param(query_params, 'id', id)
        else:
            query_params = set_query_param(query_params, 'q', city)

    return query_params

@click.command()
@click.option('--city', '-c', default="", help='Name of the City')
@click.option('--id', '-i', default="", help='OpenWeather ID of the City ')
@click.option('--api-key', '-a', default="", help='OpenWeather API Key')
@click.option('--lang', '-l', default="es", help='Set request lenguage')
@click.option('--units', '-u', default='metric', help='Unit format. The default format is metric',
type=click.Choice(['metric', 'imperial']))
@click.option('--cnt-loc', '-cl', is_flag=True, help='Use current location')
def main(city, id, api_key, lang, units, cnt_loc):    
    
    params = query_builder(city, id, apikey, lang, units, cnt_loc)
    data = get_json(params)
    display_data(data)

if __name__ == "__main__":
	main()