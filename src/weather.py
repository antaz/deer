import urllib.request
import json
import re


print("Loading the weather module...")

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
    country  : str     # Display country (for weird city names).
    info     : str     # Weather report.

    """

    def __init__(self, query: str) -> None:

        m = re.search(r'(weather) (.*)\b', query)

        try:
            self.city = m.group(2).strip().replace(" ", "%20")

        except Exception:
            self.info = "It's `.weather CITY`, bro."

        else:
            self.query_wttrin()


    def query_wttrin(self):

        self.URL = 'https://wttr.in/{}?format=j2'.format(self.city) 
        # format=j1 returns hourly info, which is overkill

        try:
            with urllib.request.urlopen(self.URL) as f:
                data = json.loads(f.read())
        except Exception as e:
            self.info = f"gtfo: error {e}"
            return
            
        self.parse_json(data)


    def parse_json(self, data: dict):

        self.curr_temp = data['current_condition'][0]['temp_C']
        self.curr_desc = data['current_condition'][0]['weatherDesc'][0]['value']
        self.precip_mm = data['current_condition'][0]['precipMM']
        self.l_c       = data['weather'][0]['mintempC']
        self.h_c       = data['weather'][0]['maxtempC']
        self.country   = data['nearest_area'][0]['country'][0]['value']

        self.info =  (
            f"{self.curr_desc} over in "
            f"{self.city.capitalize()}, {self.country}. "
            f"{self.curr_temp}°C [{self.l_c}, {self.h_c}]°C."
        )


    def __repr__(self):

        return self.info


if __name__ == '__main__':

    city = Weather("Toulouse")
    print(city.__str__())
