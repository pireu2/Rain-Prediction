# Rain Prediction Raspberrypi 

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
### Testing sensors
```shell script
pyhon tests/test.py
```
