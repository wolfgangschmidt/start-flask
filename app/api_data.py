
import requests


def get_char_data():
    char_data_list = []
    total = []
    page = requests.get('https://swapi.dev/api/people/').json()
    while "next" in page:
        result = page['results']
        page_data = []
        for res in result:
            char_dict = {}
            char_dict['name'] = res['name']
            char_dict['gender'] = res['gender']
            char_dict['height'] = res['height']
            char_dict['weight'] = res['mass']
            char_dict['homeworld'] = res['homeworld']
            char_dict['starship'] = []
            char_dict['films'] = []
            char_dict['vehicles'] = []
            for ship in res['starships']:
                char_dict['starship'].append(requests.get(ship).json()['name'])
            for films in res['films']:
                char_dict['films'].append(requests.get(films).json()['title'])
            for vehicles in res['vehicles']:
                char_dict['vehicles'].append(requests.get(vehicles).json()['name'])
            total.append(char_dict)
        try:
            page = requests.get(page['next']).json()
        except:
            break
    return total


def get_ship_data():
    ship_data_list = []

    page = requests.get('https://swapi.dev/api/starships/').json()
    while "next" in page:
        result = page['results']
        #page_data = []
        for ship in result:
            ship_dict = {}
            ship_dict['name'] = ship['name']
            ship_dict['class'] = ship['starship_class']
            ship_dict['cost'] = ship['cost_in_credits']
            try:
                ship_dict['rating'] = float(ship['hyperdrive_rating']) / float(ship['cost_in_credits'])
            except:
                ship_dict['rating'] = 0
            ship_dict['drive'] = ship['hyperdrive_rating']

            ship_data_list.append(ship_dict)
        try:
            page = requests.get(page['next']).json()
        except:
            break


    return ship_data_list
