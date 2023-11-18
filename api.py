import requests
import csv
import re
from datetime import datetime
from constants.constants import API_OUTPUT_FILE, MODIFIED_OUTPUT_FILE


def is_yyyymmdd_format(date: str):
    pattern = r"(\d{4})-(\d{2})-(\d{2})"
    numbers = re.findall(pattern, date)
    if not re.match(pattern, date):
        return False
    if int(numbers[0][1]) > 12 or int(numbers[0][2]) > 31:
        return False
    return True


def get_data(start_date: str, end_date: str):
    if not is_yyyymmdd_format(start_date) or not is_yyyymmdd_format(end_date):
        return "Error"
    url = "https://archive-api.open-meteo.com/v1/archive?"
    params = {
        "latitude": 46.77,
        "longitude": 23.62,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": [
            "temperature_2m",
            "dew_point_2m",
            "relative_humidity_2m",
            "surface_pressure",
            "shortwave_radiation",
            "precipitation",
        ],
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return "Error"


def output_csv(data):
    with open(API_OUTPUT_FILE, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data["hourly"].keys())
        writer.writeheader()
        for row in zip(*data["hourly"].values()):
            writer.writerow(dict(zip(data["hourly"].keys(), row)))

def shift():
    with open(API_OUTPUT_FILE, "r") as file:
        reader = csv.DictReader(file)
        data = list(reader)

    data = sorted(data, key = lambda x:datetime.strptime(x["time"], "%Y-%m-%dT%H:%M"))

    for i in range(len(data)):
        data[i]["precipitation_1h"] = data[i+1]["precipitation"] if i < len(data) - 1 else 0.0
        data[i]["precipitation_6h"] = data[i+6]["precipitation"] if i < len(data) - 6  else 0.0
        data[i]["precipitation_12h"] = data[i+12]["precipitation"] if i < len(data) - 12 else 0.0
        data[i]["precipitation_24h"] = data[i+24]["precipitation"] if i < len(data) - 24 else 0.0

    fields = data[0].keys()

    with open(MODIFIED_OUTPUT_FILE, "w") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)


def main():
    # data = get_data("2013-11-01", "2023-11-01")
    # if data == "Error":
    #     return
    # output_csv(data)
    shift()


if __name__ == "__main__":
    main()
