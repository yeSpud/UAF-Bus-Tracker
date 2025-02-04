import requests
from datetime import datetime
import time

stop_dict = {}
morning_route_start = datetime(hour=7, minute=30, second=0, microsecond=0, year=1, month=1, day=1).time()
night_route_start = datetime(hour=18, minute=0, second=0, microsecond=0, year=1, month=1, day=1).time()
night_route_end = datetime(hour=21, minute=0, second=0, microsecond=0, year=1, month=1, day=1).time()

class Stop:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.arrived = False

    def __str__(self):
        return f"{self.name} ({self.id}): {self.arrived}"

def get_night_data():
    data = requests.get("https://buswhere.com/uaf/routes/night_route",
                        headers={"Accept": "application/json"})
    json = data.json()
    stop_etas: dict = json["stop_eta"]
    for stop_eta in stop_etas.keys():
        print(f"Checking {stop_dict[stop_eta].name}")
        if stop_etas[stop_eta] == "arrived":
            print(f"Arrived at stop {stop_dict[stop_eta].name}")

            # Only rest to true if it wasnt already marked as such
            if not stop_dict[stop_eta].arrived:
                stop_dict[stop_eta].arrived = True
        else:
            stop_dict[stop_eta].arrived = False

# Start by getting the initialization data
# FIXME Buswhere gets rid of morning routes after 6!

print(stop_dict.keys())
print(f"Time: {datetime.now().time()}")

while (True):
    current_time = datetime.now().time()
    if night_route_start<= current_time < night_route_end:
        get_night_data()

    time.sleep(5)

# TODO Loop though each update and log if its arrived or not

