import requests
from datetime import datetime
import time

from database import Stop, Arrival, db

# stop_list = []
morning_route_start = datetime(hour=7, minute=30, second=0, microsecond=0, year=1, month=1, day=1).time()
night_route_start = datetime(hour=18, minute=0, second=0, microsecond=0, year=1, month=1, day=1).time()
night_route_end = datetime(hour=22, minute=00, second=0, microsecond=0, year=1, month=1, day=1).time()

def get_night_data():
    data = requests.get("https://buswhere.com/uaf/routes/night_route",
                        headers={"Accept": "application/json"})
    json = data.json()
    stop_etas: dict = json["stop_eta"]
    for stop_id in stop_etas.keys():
        stop = Stop.get_by_id(stop_id)
        # print(f"Checking {stop.name}") # todo better logger
        if stop_etas[stop_id] == "arrived":
            print(f"Arrived at stop {stop.name} at {datetime.now().time()}")

            # Only rest to true if it wasn't already marked as such
            #if not stop_dict[stop_id].arrived:
            Arrival.create(stop=stop, time=datetime.now().timestamp())
            #    stop_dict[stop_id].arrived = True
        #else:
            #stop_dict[stop_id].arrived = False

# Start by getting the initialization data
# FIXME Buswhere gets rid of morning routes after 6!

try:
    db.connect()
    while True:
        current_time = datetime.now().time()
        if night_route_start <= current_time < night_route_end:
            get_night_data()

        time.sleep(5)
except KeyboardInterrupt:
    print("Exiting...")
except Exception as e:
    print(e)

db.close()


# TODO Loop though each update and log if its arrived or not

