from weather import Weather

import urllib.request as request
import json

def test_always_true():
    assert True



def test_json_content():

    with open("weather/03022022.json", "r") as f:
        data = json.loads(f.read())

    assert data['current_condition'][0]['temp_C']
    assert data['current_condition'][0]['weatherDesc'][0]['value']
    assert data['current_condition'][0]['precipMM']
    assert data['weather'][0]['mintempC']
    assert data['weather'][0]['maxtempC']



def test_wttr_response():

    URL = 'https://wttr.in/{}?format=j2'.format("New York")
    URL = URL.strip().replace(' ', '%20')

    with request.urlopen(URL) as f:
        raw = f.read()
    data = json.loads(raw)

    assert isinstance(data, dict)



