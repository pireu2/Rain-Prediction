import tensorflow as tf
import numpy as np
import shutil
import os
from random import shuffle
from tensorflow.keras.models import load_model
from util.data import prepare_data, read_data
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from constants.constants import NORMALIZED_DATA, TEST_SIZE, AI_MODEL_PATH, EPOCHS_NUMBER

class RainPrediction:
    def __init__(self, data=None, header=None):
        self.models = {}
        self.data = data
        self.header = header
        # self.data = shuffle(self.data)
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
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_shape=(len(self.feature_indices),)),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(len(self.class_names), activation='softmax')
        ])
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        self.models[target_variable] = model
        return model

    def save_model(self, target_variable: str):
        model = self.models[target_variable]
        model.save(os.path.join(AI_MODEL_PATH, f"{target_variable}.keras"))

    def train_model(self, target_variable: str):
        model = self.models[target_variable]
        target_index = self.header.index(target_variable)
        x_train, y_train = prepare_data(self.train_data, self.feature_indices, target_index)
        x_test, y_test = prepare_data(self.test_data, self.feature_indices, target_index)

        # Compute class weights
        y_train_labels = [row[target_index] for row in self.train_data]
        class_weights = compute_class_weight('balanced', classes=np.unique(y_train_labels), y=y_train_labels)
        class_weight_dict = {i: weight for i, weight in enumerate(class_weights)}

        # Train the model with class weights
        model.fit(x_train, y_train, epochs=EPOCHS_NUMBER, class_weight=class_weight_dict)
        test_loss, test_accuracy = model.evaluate(x_test, y_test)
        print(f"Accuracy: {test_accuracy}")

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
            model_path = os.path.join(AI_MODEL_PATH, f"{target_variable}.keras")
            try:
                self.models[target_variable] = load_model(model_path)
                self.models[target_variable].compile(
                    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
                    loss="sparse_categorical_crossentropy",
                    metrics=["accuracy"],
                )
            except Exception as e:
                print(f"Error loading model {model_path}: {e}")

    def make_prediction(self, target_variable: str, data) -> str:
        print("Model prediction")
        if target_variable not in self.models:
            print("Error")
            return "Error"
        data_array = np.array(list(data.values())).reshape(1, -1)
        print(f"Input data: {data_array}")
        prediction = self.models[target_variable].predict(data_array)
        print(f"Raw prediction output: {prediction}")
        predicted_class = np.argmax(prediction)
        print(f"Predicted class: {predicted_class}")
        return self.class_names[predicted_class]

    def remove_models_from_disk(self):
        try:
            for filename in os.listdir(AI_MODEL_PATH):
                file_path = os.path.join(AI_MODEL_PATH, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error cleaning directory {AI_MODEL_PATH}: {e}")


def main():
    data, header = read_data(NORMALIZED_DATA)
    rain_prediction = RainPrediction(data, header)
    rain_prediction.remove_models_from_disk()
    rain_prediction.create_and_train_all_models()
    rain_prediction.save_all_models()


if __name__ == "__main__":
    main()
