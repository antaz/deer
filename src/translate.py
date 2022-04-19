import json, re
import requests

print('Loading the translation module')

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

        m = re.search(r'(fr) (.*)$', query)

        try:
            self.query = m.group(2).strip()

        except Exception:
            self.translation = "`.fr TERM`."

        else:
            self.translate()

    def translate(self):
        Translate.BODY['q'] = self.query
        r = requests.post(Translate.API_ENDPOINT, headers=Translate.HEADERS, data=json.dumps(Translate.BODY))
        self.translation = r.json()['translatedText']

    def __repr__(self):
        return self.translation
