import re
import json
import urllib


class UrbanDictionary:
    def __init__(self, query):
        m = re.search(r"(ud) (.*)$", query)

        try:
            self.term = m.group(2).strip().replace(" ", "%20")

        except Exception:
            self.definition = "It's `.ud TERM`, bro."

        else:
            self.query_ud()

    def query_ud(self):
        URL = f"https://api.urbandictionary.com/v0/define?term={self.term}"

        try:
            with urllib.request.urlopen(URL) as f:
                data = json.loads(f.read())
            self.definition = data["list"][0]["definition"]

        except Exception as e:
            print(e)
            self.definition = "Not found."

    def __repr__(self):
        return self.definition
