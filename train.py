import csv
import tensorflow as tf
import numpy as np
from util.data import prepare_data, read_data
from sklearn.model_selection import train_test_split
from constants.constants import NORMALIZED_DATA, TEST_SIZE, AI_MODEL_PATH


class RainPrediction:
    def __init__(self, data, header):
        self.models = {}
        self.data = data
        self.header = header
        self.train_data, self.test_data = train_test_split(
            self.data, test_size=TEST_SIZE
        )
        self.class_names = [
            "No Rain",
            "Light Rain",
            "Moderate Rain",
            "Heavy Rain",
            "Violent Rain",
        ]
        self.target_variables = [
            "precipitation_1h",
            "precipitation_6h",
            "precipitation_12h",
            "precipitation_24h",
        ]
        self.feature_indices = [
            self.header.index(feature)
            for feature in [
                "temperature_2m",
                "dew_point_2m",
                "relative_humidity_2m",
                "surface_pressure",
                "shortwave_radiation",
            ]
        ]

    def create_model(self, target_variable: str):
        model = tf.keras.models.Sequential(
            [
                tf.keras.Input(shape=(len(self.feature_indices),)),
                tf.keras.layers.Dense(16, activation="relu"),
                tf.keras.layers.Dense(32, activation="relu"),
                tf.keras.layers.Dense(64, activation="relu"),
                tf.keras.layers.Dense(128, activation="relu"),
                tf.keras.layers.Dropout(0.4),
                tf.keras.layers.Dense(5, activation="softmax"),
            ]
        )
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        self.models[target_variable] = model
        return model

    def save_model(self, target_variable: str):
        model = self.models[target_variable]
        model.save(AI_MODEL_PATH + str(target_variable), save_format="tf")

    def train_model(self, target_variable: str):
        model = self.models[target_variable]
        index = self.header.index(target_variable)
        x_train, y_train = prepare_data(self.train_data, self.feature_indices, index)
        x_test, y_test = prepare_data(self.test_data, self.feature_indices, index)

        model.fit(x_train, y_train, epochs=3)
        test_loss, tess_accuracy = model.evaluate(x_test, y_test)
        print(f"Accuracy: {tess_accuracy}")

    def create_and_train_all_models(self):
        for target_variable in self.target_variables:
            self.create_model(target_variable)
            self.train_model(target_variable)
            self.save_model(target_variable)

    def make_prediction(self, target_variable: str, data):
        print("Model prediction")
        if target_variable not in self.models:
            print("Error")
            return
        prediction = self.models[target_variable].predict(data)
        print(f"Prediction=> {self.class_names[np.argmax(prediction)]}")


def main():
    data, header = read_data(NORMALIZED_DATA)
    rain_prediction = RainPrediction(data, header)
    rain_prediction.create_and_train_all_models()


if __name__ == "__main__":
    main()
