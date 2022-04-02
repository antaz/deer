import urllib.request
import json


class Weather:
    """ Weather class.

    Get the current weather for a place.
    Queries wttr.in for JSON response
    
    Attributes:

    curr_temp: str     # Current Temperature in Celcius
    curr_desc: str     # Description of current weather (sunny, cloudy...)
    precip_mm: str     # Precipitation in milimeters
    l_c      : str     # Lowest temperature in Celcius
    h_c      : str     # Highest temperature in Celcius

    """

    def __init__(self, city: str) -> None:

        self.city = city.strip().replace(" ", "%20")
        self.query_wttrin()


    def query_wttrin(self):

        self.URL = 'https://wttr.in/{}?format=j2'.format(self.city) 
        # format=j1 returns hourly info, which is overkill

        with urllib.request.urlopen(self.URL) as f:
            data = json.loads(f.read())

        self.parse_json(data)


    def parse_json(self, data: dict):

        self.curr_temp = data['current_condition'][0]['temp_C']
        self.curr_desc = data['current_condition'][0]['weatherDesc'][0]['value']
        self.precip_mm = data['current_condition'][0]['precipMM']
        self.l_c       = data['weather'][0]['mintempC']
        self.h_c       = data['weather'][0]['maxtempC']


    def __repr__(self):
        info =  f"It's {self.curr_desc.lower()} as fuck over in " + \
            f"{self.city} rn.\n{self.curr_temp}°C [{self.l_c}, {self.h_c}]°C."
        return info


if __name__ == '__main__':

    city = Weather("Toulouse")
    print(city.__str__())
