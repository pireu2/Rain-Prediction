from dataclasses import dataclass
from enum import Enum
from ai.train import RainPrediction
from util.data import normalize_sensors


@dataclass
class SensorData:
    temperature: float
    humidity: float
    pressure: float
    luminosity: float
    dewpoint: float


class PredictionType(Enum):
    ONE_HOUR = 1
    SIX_HOUR = 6
    TWELVE_HOUR = 12
    TWENTY_FOUR_HOUR = 24


def load_all_models():
    rain_prediction = RainPrediction()
    rain_prediction.load_all_models()

    return rain_prediction


def predict(
    sensorData: SensorData,
    predictionType: PredictionType,
    rain_prediction: RainPrediction,
) -> str:
    prediction = ""
    data = {
        "temperature": sensorData.temperature,
        "pressure": sensorData.pressure,
        "humidity": sensorData.humidity,
        "dewpoint": sensorData.dewpoint,
        "luminosity": sensorData.luminosity,
    }

    if predictionType == PredictionType.ONE_HOUR:
        prediction = rain_prediction.make_prediction(
            "precipitation_1h", normalize_sensors(data)
        )
    elif predictionType == PredictionType.SIX_HOUR:
        prediction = rain_prediction.make_prediction(
            "precipitation_6h", normalize_sensors(data)
        )
    elif predictionType == PredictionType.TWELVE_HOUR:
        prediction = rain_prediction.make_prediction(
            "precipitation_12h", normalize_sensors(data)
        )
    elif predictionType == PredictionType.TWENTY_FOUR_HOUR:
        prediction = rain_prediction.make_prediction(
            "precipitation_24h", normalize_sensors(data)
        )

    return prediction


def main():
    sensorData = SensorData(
        temperature=17.50,  # Example temperature in Celsius
        pressure=1000.0,  # Example pressure in hPa
        humidity=0.0,  # Example humidity in percentage
        dewpoint=100.0,  # Example dewpoint in Celsius
        luminosity=1000.0,  # Example luminosity in lux
    )
    predictionType = PredictionType.ONE_HOUR
    rain_prediction = load_all_models()
    print(predict(sensorData, predictionType, rain_prediction))


if __name__ == "__main__":
    main()
