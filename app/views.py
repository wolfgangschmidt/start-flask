from flask import Flask, render_template
import sys
import requests
import json
from flask import request
from api_data import get_char_data, get_ship_data
from tests.test import get_test


app = Flask(__name__)

#these global variables are for speed

#SHIPS = get_ship_data()
#CHARACTERS = get_char_data()

FILTER = None
FILTER_KEY = None


def get_starwars_data(api_type, next_page=None):

    default_page = {"people": 'https://swapi.dev/api/people/', 
                    'starships': 'https://swapi.dev/api/starship/'}
    if not next_page:
        next_page = default_page[api_type]

    data = requests.get(next_page)

    return data


@app.route('/')
def index_view():

    return render_template('index.html')


@app.route('/characters')
def char_view():
    global CHARACTERS
    CHARACTERS = get_char_data()
    page = 0
    try:
        _next = int(request.args.get('next')) if request.args.get('next') else None
        _prev = int(request.args.get('prev')) if request.args.get('prev') else None
        current = int(request.args.get('page')) if request.args.get('page') else 0

        for key in ['films', 'homeworld', 'starship', 'vehicles']:
            filters = request.args.get(key)
            if filters:
                global FILTER_KEY
                FILTER_KEY = key
                global FILTER
                FILTER = filters.replace('_', ' ')
                break                

        if _next:
            page = current + _next
        if _prev:
             page = current - _prev
    except:
        pass

    data = CHARACTERS

    if data:
        data_list, page, filters = parse_char_data(data, None, page)
        return render_template('character.html', 
                                    data={
                                        'data':data_list, 
                                        'page': page, 
                                        'filters': filters, 
                                        "current_filter": FILTER
                                        }
                               )
    return render_template('character.html', data={'data':{'Error': "this is Unatural", 'filters': None}})


@app.route('/ships')
def ship_view():
    global SHIPS
    SHIPS = get_ship_data()
    data = sorted(SHIPS, key = lambda i: (i['drive']), reverse=False)
    return render_template('ships.html', data={'data':data})



def parse_char_data(data, filters=None, start=0):
    ordered_list = sorted(data, key = lambda i: (i['name'], 
                                                      i['gender'], 
                                                      i['weight'], 
                                                      i['height']))
    filters_options = get_filters(ordered_list)
    if FILTER and FILTER_KEY:
        ordered_list = [x for x in ordered_list if FILTER in x[FILTER_KEY]]
    return ordered_list[start: start+10], start, filters_options


def get_filters(data_lists):

    filters = {'films': [], 'homeworlds': [], 'starships': [], 'vehicles': []}
    films = [x['films'] for x in data_lists]
    homeworld = [x['homeworld'] for x in data_lists]
    starship = [x['starship'] for x in data_lists]
    vehicles = [x['vehicles'] for x in data_lists]
    for key, values in {'films': films,  
            'starships': starship, 
            'vehicles': vehicles}.items():
        for items  in values:
            for item in items:
                new_item = item.replace(' ', '_')
                filters[key].append(new_item)
        filters[key] = list(set(filters[key]))
    filters['homeworlds'] = list(set(homeworld))
    return filters


if __name__ == '__main__':
   app.run()
