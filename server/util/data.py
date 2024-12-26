import csv
import numpy as np
from datetime import datetime
from constants.constants import (
    NORMALIZED_DATA,
    API_OUTPUT_FILE,
    TEMP_N,
    PRESSURE_N,
    DEWPOINT_N,
    HUMIDITY_N,
    LUMINOSITY_N,
)


def read_data(path: str):
    with open(path, "r") as file:
        reader = csv.DictReader(file)
        header = list(next(reader))
        data = [list(row.values()) for row in reader]
    return data, header


def prepare_data(data, feature_indices, target_index: int):
    x = np.array([[float(row[i]) for i in feature_indices] for row in data])
    y = np.array([float(row[target_index]) for row in data])
    return x, y


def normalize_data(input_path: str, output_path: str):
    try:
        with open(input_path, "r") as file:
            reader = csv.DictReader(file)
            data = list(reader)
    except FileNotFoundError:
        return False

    data = sorted(data, key=lambda x: datetime.strptime(x["time"], "%Y-%m-%dT%H:%M"))

    try:
        for i in range(len(data)):
            data[i]["precipitation_1h"] = (
                data[i + 1]["precipitation"] if i < len(data) - 1 else 0.0
            )

            data[i]["precipitation_6h"] = (
                data[i + 6]["precipitation"] if i < len(data) - 6 else 0.0
            )

            data[i]["precipitation_12h"] = (
                data[i + 12]["precipitation"] if i < len(data) - 12 else 0.0
            )

            data[i]["precipitation_24h"] = (
                data[i + 24]["precipitation"] if i < len(data) - 24 else 0.0
            )
            data[i]["temperature_2m"] = float(data[i]["temperature_2m"]) / TEMP_N
            data[i]["dew_point_2m"] = float(data[i]["dew_point_2m"]) / DEWPOINT_N
            data[i]["relative_humidity_2m"] = (
                float(data[i]["relative_humidity_2m"]) / HUMIDITY_N
            )
            data[i]["surface_pressure"] = (
                float(data[i]["surface_pressure"]) / PRESSURE_N
            )
            data[i]["shortwave_radiation"] = (
                float(data[i]["shortwave_radiation"]) / LUMINOSITY_N
            )
    except (ValueError, IndexError):
        print("Data not valid")
        return False

    fields = data[0].keys()

    try:
        with open(output_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)
    except FileNotFoundError:
        return False
    return True


def normalize_sensors(data):
    normalized_data = {}
    normalized_data["temperature_2m"] = data["temperature"] / TEMP_N
    normalized_data["surface_pressure"] = data["pressure"] / PRESSURE_N
    normalized_data["relative_humidity_2m"] = data["humidity"] / HUMIDITY_N
    normalized_data["dew_point_2m"] = data["dewpoint"] / DEWPOINT_N
    normalized_data["shortwave_radiation"] = data["luminosity"] / LUMINOSITY_N
    return normalized_data


def main():
    if not normalize_data(API_OUTPUT_FILE, NORMALIZED_DATA):
        print("Could not normalize data")


if __name__ == "__main__":
    main()
