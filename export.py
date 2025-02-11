from database import *
import shutil
from pathlib import Path
from datetime import datetime

def get_time(date: datetime) -> str:
    return f"{str(date.hour).zfill(2)}:{str(date.minute).zfill(2)}"

def print_date(day_of_week: str, date: datetime):
    print(f"{day_of_week}, {get_time(date)}")

def append_to_csv(path: str, data: str):
    file = open(path, "a")
    file.write(f"{data},")
    file.close()

db.connect()
exported_directory = "./exported"
shutil.rmtree(exported_directory, ignore_errors=True)
Path(exported_directory).mkdir(parents=True, exist_ok=True)
for route in Route.select():
    # print(f"\nExporting stops for {route.name} route")
    Path(f"{exported_directory}/{route.name}").mkdir(parents=True, exist_ok=True)
    for stop in route.stops:
        # print(f"\n{stop.name}")
        Path(f"{exported_directory}/{route.name}/{stop.name}").mkdir(parents=True, exist_ok=True)
        prev_date = None
        for arrival in stop.arrivals:
            date: datetime = arrival.time
            day_of_week = ""
            match date.weekday():
                case 0:
                    # Monday
                    day_of_week = "Monday"
                case 1:
                    # Tuesday
                    day_of_week = "Tuesday"
                case 2:
                    # Wednesday
                    day_of_week = "Wednesday"
                case 3:
                    # Thursdays
                    day_of_week = "Thursday"
                case 4:
                    # Friday
                    day_of_week = "Friday"

            # print_date(day_of_week, date)
            if prev_date is not None and prev_date.time() > date.time():
                append_to_csv(f"{exported_directory}/{route.name}/{stop.name}/{day_of_week}.csv", f"\n{get_time(date)}")
            else:
                append_to_csv(f"{exported_directory}/{route.name}/{stop.name}/{day_of_week}.csv", get_time(date))

            prev_date = date

db.close()
