#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, csv

def get_pokemon(url= 'http://pokeapi.co/api/v2/pokemon-form', offset=0):
    args= {'offset': offset} if offset else {}

    response= requests.get(url, params= args)
    if response.status_code == 200:

        payload= response.json()
        results= payload.get('results', [])

        if results:
            for pokemon in results:
                name= pokemon['name']
                print(name)
                csvWriter.writerow([name])

        next = "y"
        if next == 'y':
            if offset <= 1283:
                get_pokemon(offset= offset+20)
            

if __name__ == '__main__':
    csvFile = open("./DB/data.csv", "w",newline="")
    csvWriter = csv.writer(csvFile)
    get_pokemon()
    csvFile.close()