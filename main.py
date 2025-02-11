import logging
import os

import requests
from datetime import datetime
import time

from database import Stop, Arrival, db

morning_route_start = datetime(hour=7, minute=30, second=0, microsecond=0, year=1, month=1, day=1).time()
night_route_start = datetime(hour=18, minute=0, second=0, microsecond=0, year=1, month=1, day=1).time()
night_route_end = datetime(hour=22, minute=00, second=0, microsecond=0, year=1, month=1, day=1).time()

logger = logging.getLogger("bus-tracker")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
level = os.environ.get("LOG_LEVEL", "INFO")
logger.setLevel(level)

def parse_data(data):
    json = data.json()

    # Check that there is a stop eta
    if not json["stop_eta"]:
        # logger.warning("No stop eta")
        return

    stop_etas: dict = json["stop_eta"]
    for stop_id in stop_etas.keys():
        stop = Stop.get_by_id(stop_id)
        logger.debug(f"Checking {stop.name}")
        if stop_etas[stop_id] == "arrived":
            logger.info(f"Arrived at stop {stop.name} at {datetime.now().time()}")
            Arrival.create(stop=stop, time=datetime.now().timestamp())

def get_nenana_data():
    data = requests.get("https://buswhere.com/uaf/routes/nenana_morning", headers={"Accept": "application/json"})
    parse_data(data)

def get_yukon_data():
    y1_data = requests.get("https://buswhere.com/uaf/routes/yukon_route_bus_1", headers={"Accept": "application/json"})
    parse_data(y1_data)

    # y2_data = requests.get("https://buswhere.com/uaf/routes/yukon_route_bus_2", headers={"Accept": "application/json"})
    # parse_data(y2_data)

def get_night_data():
    data = requests.get("https://buswhere.com/uaf/routes/night_route", headers={"Accept": "application/json"})
    parse_data(data)

try:
    logger.info("Starting up")
    db.connect()
    while True:
        current_time = datetime.now().time()

        if morning_route_start <= current_time <= night_route_start:
            get_nenana_data()
            get_yukon_data()
        elif night_route_start <= current_time < night_route_end:
            get_night_data()
        else:
            logger.debug("Outside operating hours")

        time.sleep(5)
except KeyboardInterrupt:
    logger.warning("Exiting...")
except Exception as e:
    logger.error(e)

db.close()
