import requests
import re
from bs4 import BeautifulSoup
import json

from peewee import IntegrityError

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
        try:
            Stop.create(id=stop["id"], name=stop["address"], route=route)
        except IntegrityError as e:
            print("that stop already exists in the database")

db.connect()
db.create_tables([Route, Stop, Arrival])


try:
    print("Initializing nenana data")
    nenana_route = Route.create(name="Nenana")
    nenana_data = get_data("https://buswhere.com/uaf/routes/nenana_morning")
    add_to_database(nenana_data["stops"], nenana_route)
except IntegrityError as e:
    print("The nenana route already exists")

try:
    print("Initializing yukon data")
    yukon_route = Route.create(name="Yukon")
    yukon_1_data = get_data("https://buswhere.com/uaf/routes/yukon_route_bus_1")
    yukon_2_data = get_data("https://buswhere.com/uaf/routes/yukon_route_bus_2")
    add_to_database(yukon_1_data["stops"], yukon_route)
    add_to_database(yukon_2_data["stops"], yukon_route)
except IntegrityError as e:
    print("The yukon 1 route already exists")


try:
    print("Initializing night data")
    night_route = Route.create(name="Night")
    night_data = get_data("https://buswhere.com/uaf/routes/night_route")
    add_to_database(night_data["stops"], night_route)
except IntegrityError as e:
    print("The night route already exists")

db.close()