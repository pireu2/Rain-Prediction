import requests
import json
import csv
import re

def is_yyyymmdd_format(date : str):
    pattern = r"(\d{4})-(\d{2})-(\d{2})"
    numbers = re.findall(pattern, date)
    if not re.match(pattern, date):
        return False
    if int(numbers[0][1]) > 12 or int(numbers[0][2]) > 31:
        return False
    return True

def get_data(start_date : str, end_date : str):
    if not is_yyyymmdd_format(start_date) or not is_yyyymmdd_format(end_date):
        return "Error"
    url = "https://archive-api.open-meteo.com/v1/archive?"
    params = {
        "latitude": 46.77,
        "longitude": 23.62,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ["temperature_2m", "relative_humidity_2m", "rain", "weather_code", "surface_pressure"]
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json() 
        return data
    else:
        return "Error"

def output_csv(data, filename : str = "output"):
    with open(f'{filename}.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data['hourly'].keys())
        writer.writeheader()
        for row in zip(*data['hourly'].values()):
            writer.writerow(dict(zip(data['hourly'].keys(), row)))

def main():
    data = get_data('2023-10-01', '2023-10-02')
    if data == "Error":
        return
    output_csv(data)

if __name__ == '__main__':
    main()