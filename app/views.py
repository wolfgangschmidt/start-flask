from flask import Flask, render_template
import requests
from flask import request
app = Flask(__name__)

def get_starwars_character_data(next_page=None):
    if not next_page:
        next_page = 1
    data = requests.get(f'https://swapi.dev/api/people/?page={str(next_page)}')

    return data

@app.route('/')
def char_view():
    next_page = 1
    try:
        next_page = request.args.get('next')
        next_page = request.args.get('prev')

        import pdb; pdb.set_trace()
    except:
        pass

    data = get_starwars_character_data(next_page)
    if data.status_code == 200:
        data = parse_char_data(data.json()['results'])
    return render_template('index.html', data={'data':data, 'page': next_page})


def parse_char_data(data):
    data_list = []
    for character in data:
        char_dict = {}
        char_dict['name'] = character['name']
        char_dict['gender'] = character['gender']
        char_dict['height'] = character['height']
        char_dict['weight'] = character['mass']
        data_list.append(char_dict)
    
    return sorted(data_list, key = lambda i: (i['name'], i['gender'], i['weight'], i['height'])) 


if __name__ == '__main__':
   app.run()