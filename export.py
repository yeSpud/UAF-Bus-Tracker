from database import *
import shutil
import argparse
from pathlib import Path
from datetime import datetime

def get_time(date: datetime) -> str:
    return f"{str(date.hour).zfill(2)}:{str(date.minute).zfill(2)}"

def pre_populate_dict():
    d = {}
    for hour in range(7, 22):
        for minute in range(0, 60):
            d[f"{str(hour).zfill(2)}:{str(minute).zfill(2)}"] = 0
    return d


def increment_dict(dict: dict, key: str):
    if not key in dict:
        dict[key] = 1
    else:
        dict[key] += 1

def append_to_csv(path: str, data: dict):
    file = open(path, "a")
    for key, value in data.items():
        file.write(f"{key}, {value}\n")
    file.close()

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-p", "--prepopulate", required=False, action="store_true", help="Pre-populate all times to be 0")
args = parser.parse_args()

db.connect()
exported_directory = "./exported"
shutil.rmtree(exported_directory, ignore_errors=True)
Path(exported_directory).mkdir(parents=True, exist_ok=True)
for route in Route.select():
    Path(f"{exported_directory}/{route.name}").mkdir(parents=True, exist_ok=True)
    for stop in route.stops:
        Path(f"{exported_directory}/{route.name}/{stop.name}").mkdir(parents=True, exist_ok=True)

        if args.prepopulate:
            monday = pre_populate_dict()
            tuesday = pre_populate_dict()
            wednesday = pre_populate_dict()
            thursday = pre_populate_dict()
            friday = pre_populate_dict()

            m_w_f = pre_populate_dict()
            t_th = pre_populate_dict()

            all = pre_populate_dict()
            pass
        else:
            monday = {}
            tuesday = {}
            wednesday = {}
            thursday = {}
            friday = {}

            m_w_f = {}
            t_th = {}

            all = {}

        for arrival in stop.arrivals:
            date: datetime = arrival.time
            time = get_time(date)

            match date.weekday():
                case 0:
                    # Monday
                    increment_dict(monday, time)
                    increment_dict(m_w_f, time)
                case 1:
                    # Tuesday
                    increment_dict(tuesday, time)
                    increment_dict(t_th, time)
                case 2:
                    # Wednesday
                    increment_dict(wednesday, time)
                    increment_dict(m_w_f, time)
                case 3:
                    # Thursdays
                    increment_dict(thursday, time)
                    increment_dict(t_th, time)
                case 4:
                    # Friday
                    increment_dict(friday, time)
                    increment_dict(m_w_f, time)

            increment_dict(all, time)

        append_to_csv(f"{exported_directory}/{route.name}/{stop.name}/monday.csv", monday)
        append_to_csv(f"{exported_directory}/{route.name}/{stop.name}/tuesday.csv", tuesday)
        append_to_csv(f"{exported_directory}/{route.name}/{stop.name}/wednesday.csv", wednesday)
        append_to_csv(f"{exported_directory}/{route.name}/{stop.name}/thursday.csv", thursday)
        append_to_csv(f"{exported_directory}/{route.name}/{stop.name}/friday.csv", friday)

        append_to_csv(f"{exported_directory}/{route.name}/{stop.name}/monday_wednesday_friday.csv", m_w_f)
        append_to_csv(f"{exported_directory}/{route.name}/{stop.name}/tuesday_thursday.csv", t_th)

        append_to_csv(f"{exported_directory}/{route.name}/{stop.name}/all.csv", all)
db.close()
