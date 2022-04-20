import json, re
import requests

print('Loading the translation module')

class Translate:
    ''' Query an instance of libretranslate using their API '''


    def __init__(self, query: str, source: str = None, target: str = None):
        self.api_endpoint = 'https://translate.argosopentech.com'
        self.headers =  { "Content-Type": "application/json" }

        if source == 'any':
            self.query = re.search(r'(tr) (.*)$', query).group(2).strip()
            self.source = self.detect_lang(self.query)
            self.target = 'en'

        elif source == 'en':
            self.query = re.search(r'(fr) (.*)$', query).group(2).strip()
            self.target = target
            self.source = source

        self.translate()

    def detect_lang(self, query):
        self.body =  {
            'q': query,
            'format': "text"
        }
        print('query: ', query)
        r = requests.post(f"{self.api_endpoint}/detect", headers=self.headers, data=json.dumps(self.body))
        print(r)
        print(r.json())
        return r.json()[0]['language']


    def translate(self):

        self.body =  {
            'q': self.query,
            'source': self.source,
            'target': self.target,
            'format': "text"
        }

        r = requests.post(f"{self.api_endpoint}/translate", headers=self.headers, data=json.dumps(self.body))
        self.translation = r.json()['translatedText']

    def __repr__(self):
        return self.translation

if __name__=='__main__':

    translation = Translate('.tr como esta mi amor', source='any', target='fr')
    print(translation)

