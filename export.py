from database import *
import shutil
from pathlib import Path
from datetime import datetime

def get_time(date: datetime) -> str:
    return f"{str(date.hour).zfill(2)}:{str(date.minute).zfill(2)}"

def append_to_csv(path: str, data: dict):
    file = open(path, "a")
    for key, value in data.items():
        file.write(f"{key}, {value}\n")
    file.close()

db.connect()
exported_directory = "./exported"
shutil.rmtree(exported_directory, ignore_errors=True)
Path(exported_directory).mkdir(parents=True, exist_ok=True)
for route in Route.select():
    Path(f"{exported_directory}/{route.name}").mkdir(parents=True, exist_ok=True)
    for stop in route.stops:
        Path(f"{exported_directory}/{route.name}/{stop.name}").mkdir(parents=True, exist_ok=True)

        monday = {}
        tuesday = {}
        wednesday = {}
        thursday = {}
        friday = {}

        for arrival in stop.arrivals:
            date: datetime = arrival.time
            time = get_time(date)

            match date.weekday():
                case 0:
                    # Monday
                    if not time in monday:
                        monday[time] = 1
                    else:
                        monday[get_time(date)] += 1
                case 1:
                    # Tuesday
                    if not time in tuesday:
                        tuesday[time] = 1
                    else:
                        tuesday[get_time(date)] += 1
                case 2:
                    # Wednesday
                    if not time in wednesday:
                        wednesday[time] = 1
                    else:
                        wednesday[get_time(date)] += 1
                case 3:
                    # Thursdays
                    if not time in thursday:
                        thursday[time] = 1
                    else:
                        thursday[get_time(date)] += 1
                case 4:
                    # Friday
                    if not time in friday:
                        friday[time] = 1
                    else:
                        friday[get_time(date)] += 1

        append_to_csv(f"{exported_directory}/{route.name}/{stop.name}/monday.csv", monday)
        append_to_csv(f"{exported_directory}/{route.name}/{stop.name}/tuesday.csv", tuesday)
        append_to_csv(f"{exported_directory}/{route.name}/{stop.name}/wednesday.csv", wednesday)
        append_to_csv(f"{exported_directory}/{route.name}/{stop.name}/thursday.csv", thursday)
        append_to_csv(f"{exported_directory}/{route.name}/{stop.name}/friday.csv", friday)
db.close()
