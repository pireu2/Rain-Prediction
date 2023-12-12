# Rain Prediction Raspberrypi 
small summary of the project
## Motivation
This project was created for the Electronic Measurement Systems course at the Faculty of Computer Science at Technical University of Cluj-Napoca. The goal of the project was to create a neural network that predicts if it will rain in the next 1, 6, 12 or 24 hours. The neural network was trained using data from the [Open Meteo](https://open-meteo.com/) api and the data from the sensors. The sensors used for this project are [BME280](https://www.bosch-sensortec.com/products/environmental-sensors/humidity-sensors-bme280/) and [TSL2561](https://ams.com/tsl2561). The neural network was trained using the [Keras](https://keras.io/) library. The neural network was trained on a local computer and the models were saved. The models were then loaded in memory on the Raspberrypi and used for predicting the weather. The predictions were displayed on a 1602 LCD Hat with buttons. The LED on the LCD Hat turns red when the models are being loaded in memory and green when the models are loaded in memory. The LED blinks red when the data is being gathered from the sensors. The LED blinks green when the prediction is being made.
## Table of contents
- [Project Structure](#project-structure)
- [API](#api)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
    - [Installing dependencies](#installing-dependencies)
    - [Downloading data from api](#downloading-data-from-api)
    - [Normalizing data](#normalizing-data)
    - [Training and saving the models](#training-and-saving-the-models)
- [Running](#running)
    - [Testing sensors](#testing-sensors)
    - [Predicting Raining](#predicting-raining)
## Project Structure
- `ai` - package for all AI related functions and classes
    - `predict.py` - main function used for reading data from sensors and predicting 
    - `train.py` - AI network creation and training
- `constants` - package for all constants
    - `constants.py` - all constants used for this project
- `data` - folder used for storing data
   - `data.csv` - data from the api
   - `data-modified.csv` - data after categorizing and normalizing
- `models` - folder for storing all trained models
- `sensors` - package for all sensor related functions
   - `bme280.py` - functions for getting and calculating the dewpoint for the BME280 sensor
   - `tsl2561.py` - functions for getting the TSL2561 sensor
   - `lcd.py` - functions for getting the LCD
- `tests` - package for all the tests
   - `test.py` - runs all tests
   - `test_lcd.py` - test for the LCD
   - `test_sensors.py` - tests for all the sensors
- `util` - package for all utility functions
   - `api.py` - functions for requesting data from the api and writing it in memory
   - `data.py` - functions for normalizing the api data and the data from the sensors
- `requirements.txt` - list of all python packages required for running this project
- `setup.py` - setup routine for installing local packages
## API
The api used for gathering the data for the neural network is [Open Meteo](https://open-meteo.com/).
</br>
Formula used for calculated dewpoint using temperature, humidity and pressure [link](https://en.wikipedia.org/wiki/Dew_point#Calculating_the_dew_point).
## Prerequisites
- Python 3.11 
- Raspberrypi 4
- BME280 Temperature, Humidity and Pressure Sensor
- TSL2561 Light Intensity Sensor
- 1602 LCD Hat with buttons
## Setup
### Installing dependencies
```shell script
git clone https://github.com/pireu2/Rain-Prediction.git
pip install -r requirements.txt
pip install -e .
```
### Downloading data from api
```shell script
python util/api.py start_date end_date
```
start_date and end_date must be in yyyy-mm-dd format
### Normalizing data
```shell script
python util/data.py
```
### Training and saving the models
```shell script
python ai/train.py
```
## Running
### Testing sensors
```shell script
pyhon tests/test.py
```
If the tests raise errors, the i2c address of the senors can be changed in `constants/constants.py`.
### Predicting Raining
Before predicting, the models should be trained and saved.
```shell script
pyhon ai/predict.py
```
After running, the LED should turn red and after the models are loaded in memory, it should turn green.</br>
For predictions, press the buttons on the LCD Hat:
- `1h prediction`: up button
- `6h prediction`: right button
- `12h prediction`: down button
- `24h prediction`: left button
- `exit`: select button

## Light Intensity
| Illuminance          | Example                                                 |
|----------------------|---------------------------------------------------------|
| 0.002 lux            | Moonless clear night sky                                |
| 0.2 lux              | Design minimum for emergency lighting (AS2293).         |
| 0.27 - 1 lux         | Full moon on a clear night                              |
| 3.4 lux              | Dark limit of civil twilight under a clear sky          |
| 50 lux               | Family living room                                      |
| 80 lux               | Hallway/toilet                                          |
| 100 lux              | Very dark overcast day                                  |
| 300 - 500 lux        | Sunrise or sunset on a clear day. Well-lit office area. |
| 1,000 lux            | Overcast day; typical TV studio lighting                |
| 10,000 - 25,000 lux  | Full daylight (not direct sun)                          |
| 32,000 - 130,000 lux | Direct sunlight                                         |
