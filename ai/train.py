import tensorflow as tf
import numpy as np
from util.data import prepare_data, read_data
from sklearn.model_selection import train_test_split
from constants.constants import NORMALIZED_DATA, TEST_SIZE, AI_MODEL_PATH, EPOCHS_NUMBER


class RainPrediction:
    def __init__(self, data=None, header=None):
        self.models = {}
        self.data = data
        self.header = header
        if self.data and self.header:
            self.train_data, self.test_data = train_test_split(
                self.data, test_size=TEST_SIZE
            )
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

        model.fit(x_train, y_train, epochs=1)
        test_loss, tess_accuracy = model.evaluate(x_test, y_test)
        print(f"Accuracy: {tess_accuracy}")

    def create_and_train_all_models(self):
        for target_variable in self.target_variables:
            self.create_model(target_variable)
            self.train_model(target_variable)
            self.save_model(target_variable)

    def save_all_models(self):
        for target_variable in self.target_variables:
            self.save_model(target_variable)

    def load_all_models(self):
        for target_variable in self.target_variables:
            model = tf.keras.models.load_model(AI_MODEL_PATH + target_variable)
            self.models[target_variable] = model

    def make_prediction(self, target_variable: str, data) -> str:
        print("Model prediction")
        if target_variable not in self.models:
            print("Error")
            return
        data_array = np.array(list(data.values())).reshape(1, -1)
        prediction = self.models[target_variable].predict(data_array)
        predicted_class = np.argmax(prediction)
        return self.class_names[predicted_class]


def main():
    data, header = read_data(NORMALIZED_DATA)
    rain_prediction = RainPrediction(data, header)
    rain_prediction.create_and_train_all_models()
    rain_prediction.save_all_models()


if __name__ == "__main__":
    main()
