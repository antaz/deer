import json
import requests

class Translate:
    ''' Query an instance of libretranslate using their API '''

    API_ENDPOINT = 'https://translate.argosopentech.com/translate'
    HEADERS =  { "Content-Type": "application/json" }
    BODY =  {
        'q': "Holly crap",
        'source': "en",
        'target': "fr",
        'format': "text"
    }

    def __init__(self, query: str):
        self.query = query
        self.translate()
    def translate(self):
        Translate.BODY['q'] = self.query
        r = requests.post(Translate.API_ENDPOINT, headers=Translate.HEADERS, data=json.dumps(Translate.BODY))
        self.translation = r.json()['translatedText']
    def __repr__(self):
        return self.translation


def main():
    translation = Translate("What's up, bro?")
    print(translation)

main()
