import requests
import re
from bs4 import BeautifulSoup
import json

from database import Route, Stop, Arrival, db


def get_data(url: str):
    data = requests.get(url)
    html = BeautifulSoup(data.text, "html.parser")
    scripts = html.find_all("script")
    for script in scripts:
        string = str(script.text).strip()
        if ("Maps.data = {" in string):
            regex = re.compile(r"Maps\.data = (.*?);")
            foo = regex.match(string)
            if foo is not None:
                return json.loads(foo.group(1))

    return json.loads("{}")

def add_to_database(stops, route):
    for stop in stops:
        print(f"Adding stop {stop["address"]}")
        Stop.create(id=stop["id"], name=stop["address"], route=route)

db.connect()
db.create_tables([Route, Stop, Arrival])


'''
print("Loading nenana data")
nenana = get_data("https://buswhere.com/uaf/routes/nenana_morning")
add_to_dict(nenana["stops"])

# TODO Yukon data
'''

print("Initializing night data")
night_route = Route.create(name="Night")
night_data = get_data("https://buswhere.com/uaf/routes/night_route")
add_to_database(night_data["stops"], night_route)

db.close()