# Rain Prediction

## Motivation

The goal of the project was to create a neural network that predicts if it will rain in the next 1, 6, 12 or 24 hours. The neural network was trained using data from the [Open Meteo](https://open-meteo.com/) api and the data from the sensors. The sensors used for this project are [BME280](https://www.bosch-sensortec.com/products/environmental-sensors/humidity-sensors-bme280/) and [TSL2561](https://ams.com/tsl2561). The neural network was trained using the [Keras](https://keras.io/) library. The neural network is trained on the server and saved. The models are loaded in memory on the server on startup and used for predicting the weather. The predictions are displayed on the client on a 1602 LCD with buttons.

## Table of contents

- [Project Structure](#project-structure)
- [API](#api)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Installing dependencies for the server](#installing-dependencies-for-the-server)
  - [Installing dependencies for the client](#installing-dependencies-for-the-client)
  - [Downloading data from api](#downloading-data-from-api)
  - [Normalizing data](#normalizing-data)
  - [Training and saving the models](#training-and-saving-the-models)
- [Running](#running)
  - [Running the server](#running-the-server)
  - [Running the client](#running-the-client)

## Project Structure

- `client`
  - `main.ino` - C++ code for the client side of the application intended to run on a ESP32 with the sensors and lcd connected to the i2c interface
- `server`
  - `ai` - package for all AI related functions and classes
    - `predict.py` - main function used for reading data from sensors and predicting
    - `train.py` - AI network creation and training
  - `constants` - package for all constants
    - `constants.py` - all constants used for this project
  - `data` - folder used for storing data
    - `data.csv` - data from the api
    - `data-modified.csv` - data after categorizing and normalizing
  - `models` - folder for storing all trained models
  - `util` - package for all utility functions
    - `api.py` - functions for requesting data from the api and writing it in memory
    - `data.py` - functions for normalizing the api data and the data from the sensors
  - `requirements.txt` - list of all python packages required for running this project
  - `server.py` - flask server accepting requests for predictions
  - `setup.py` - setup routine for installing local packages

## API

The api used for gathering the data for the neural network is [Open Meteo](https://open-meteo.com/).
</br>
Formula used for calculated dewpoint using temperature, humidity and pressure [link](https://en.wikipedia.org/wiki/Dew_point#Calculating_the_dew_point).

## Prerequisites

- Python 3.12
- ESP32 or Arduino Mega
- BME280 Temperature, Humidity and Pressure Sensor
- TSL2561 Light Intensity Sensor
- 1602 LCD with buttons
- Computer running the server

## Setup

### Installing dependencies for the server

```shell script
git clone https://github.com/pireu2/Rain-Prediction.git
pip install -r server/requirements.txt
pip install -e server/.
```

### Installing dependencies for the client

Install the C++ dependencies:

- [ArduinoJson](https://github.com/bblanchon/ArduinoJson)
- [Adafruit_BME280](https://github.com/adafruit/Adafruit_BME280_Library)
- [Adafruit_TSL2561_U](https://github.com/adafruit/Adafruit_TSL2561)
- [Adafruit_RGBLCDShield](https://github.com/adafruit/Adafruit-RGB-LCD-Shield-Library)

### Downloading data from api

```shell script
python server/util/api.py start_date end_date
```

start_date and end_date must be in yyyy-mm-dd format

### Normalizing data

```shell script
python server/util/data.py
```

### Training and saving the models

```shell script
python server/ai/train.py
```

## Running

### Running the server

```shell script
pyhon server/server.py
```

The server will default to the 5000 port.

### Running the client

Configure the SSID and Passoword and the local ip address of the server running the server side of the application.<br>

Upload the C++ code to the ESP32 or Arduino Mega.<br>
Use the LCD buttons for navigation and predictions.

- `up button` Get sensor data
- `down button` Predict current sensor data
- `right button` Increase the prediction interval
- `left button` Decrease the prediction interval
- `select button` Display current sensor data
