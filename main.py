import requests
from bs4 import BeautifulSoup
import re
import json

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

# Start by getting the bus where data
nenana = get_data("https://buswhere.com/uaf/routes/nenana_morning")
# print(nenana)
for stop in nenana["stops"]:
    if stop["eta"] == "Arrived":
        print(f"Arrived at stop {stop["address"]}")
