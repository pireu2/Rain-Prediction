import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from flask import Flask, request, jsonify
from ai.predict import predict, SensorData, PredictionType, load_all_models

app = Flask(__name__)

rain_prediction = load_all_models()


@app.route("/predict", methods=["POST"])
def predict_rain():
    data = request.json
    sensor_data = SensorData(
        temperature=data["temperature"],
        humidity=data["humidity"],
        pressure=data["pressure"],
        luminosity=data["luminosity"],
        dewpoint=data["dewpoint"],
    )
    prediction_type = PredictionType[data["prediction_type"]]
    prediction = predict(sensor_data, prediction_type, rain_prediction)
    return jsonify({"prediction": float(prediction)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
