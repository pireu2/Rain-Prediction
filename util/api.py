import sys
import requests
import csv
import re
from constants.constants import API_OUTPUT_FILE


def is_yyyymmdd_format(date: str) -> bool:
    pattern = r"(\d{4})-(\d{2})-(\d{2})"
    numbers = re.findall(pattern, date)
    if not re.match(pattern, date):
        return False
    if int(numbers[0][1]) > 12 or int(numbers[0][2]) > 31:
        return False
    return True


def get_data(start_date: str, end_date: str):
    if not is_yyyymmdd_format(start_date) or not is_yyyymmdd_format(end_date):
        raise ConnectionError
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
        raise ConnectionError


def output_api(data):
    with open(API_OUTPUT_FILE, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data["hourly"].keys())
        writer.writeheader()
        for row in zip(*data["hourly"].values()):
            writer.writerow(dict(zip(data["hourly"].keys(), row)))


def main():
    if len(sys.argv) != 3:
        print("Usage: python api.py yyyy-mm-dd yyyy-mm-dd")
        return
    try:
        data = get_data(sys.argv[1], sys.argv[2])
    except ConnectionError:
        return
    output_api(data)


if __name__ == "__main__":
    main()
