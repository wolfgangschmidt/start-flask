import json
import pytest
from mock import patch
from tests import test_data
from tests import test_data_ships

def get_test():

    return test_data.data, test_data_ships.data

@patch('views.get_char_data')
@patch('views.get_ship_data')
def test_index(_SHIP, _CHARACTER, app, client):
    _SHIP.return_value = get_test()[0]
    _CHARACTER.return_value = get_test()[1]
    res = client.get('/')
    assert res.status_code == 200


@patch('views.get_char_data')
@patch('views.get_ship_data')
def test_ships(_SHIP, _CHARACTER, app, client):
    _SHIP.return_value = get_test()[0]
    _CHARACTER.return_value = get_test()[1]
    res = client.get('/ships')
    assert res.status_code == 200


@patch('views.get_char_data')
@patch('views.get_ship_data')
def test_characters(_SHIP, _CHARACTER, app, client):
    _SHIP.return_value = get_test()[0]
    _CHARACTER.return_value = get_test()[1]
    res = client.get('/characters')
    assert res.status_code == 200