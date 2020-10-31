from flask import Flask, render_template
import requests
import json
from flask import request
from api_data import get_char_data, get_ship_data
import test_data
import test_data_ships
app = Flask(__name__)


#SHIPS = get_ship_data()
#CHARACTERS = get_char_data()

def get_test():

    return test_data, test_data_ships

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
    page = 0
    try:
        _next = int(request.args.get('next')) if request.args.get('next') else None
        _prev = int(request.args.get('prev')) if request.args.get('prev') else None
        current = int(request.args.get('page')) if request.args.get('page') else 0
        if _next:
            page = current + _next
        if _prev:
             page = current - _prev
    except:
        return render_template('character.html', data={'data':{'Error': "this is Unatural"}})

    data = get_test()[0]
    if data:
        data_list, page = parse_char_data(data, None, page)
    return render_template('character.html', data={'data':data_list, 'page': page})


@app.route('/ships')
def ship_view():

    data = get_test()[1]
    if data:
        data = parse_ship_data(data)
    return render_template('ships.html', data={'data':data})



def parse_char_data(data, filters=None, start=0):
    ordered_list = sorted(data.data, key = lambda i: (i['name'], 
                                                      i['gender'], 
                                                      i['weight'], 
                                                      i['height']))
    if filters:
        ordered_list = [x for x in ordered_list if filters in x]
    return ordered_list[start: start+10], start


def parse_ship_data(data):
    data_list =  []
    data_list = get_test()[1].data

    return sorted(data_list, key = lambda i: (i['rating']), reverse=True)


if __name__ == '__main__':
   app.run()