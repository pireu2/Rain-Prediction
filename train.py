import csv
import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler

from constants.constants import MODIFIED_OUTPUT_FILE, TEST_SIZE, AI_MODEL_PATH


def prepare_data(data, feature_indices, target_index):
    x = np.array([[float(row[i]) for i in feature_indices] for row in data])
    y = np.array([float(row[target_index]) for row in data])
    return x,y

def create_model(input_dimension):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(128, input_dim=input_dimension, activation="relu"),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dropout(0.4),
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss=custom_loss,
        metrics=["mean_squared_error"]
    )
    return model

def custom_loss(y_true, y_pred):
    y_true_original = tf.keras.backend.exp(y_true) - 1
    y_pred_original = tf.keras.backend.exp(y_pred) - 1

    reward_component = tf.keras.backend.mean(tf.keras.backend.square(y_true_original - y_pred_original), axis=-1)
    penalty_component = tf.keras.backend.mean(tf.keras.backend.square(tf.keras.backend.minimum(y_true_original, 0)), axis = -1)

    alpha = 0.8
    combined_loss = alpha * reward_component + (1-alpha) * penalty_component

    return combined_loss

def main():
    with open(MODIFIED_OUTPUT_FILE, "r") as file:
        reader = csv.DictReader(file)
        header = list(next(reader))
        data = [list(row.values()) for row in reader]


    train_data, test_data = train_test_split(data, test_size=TEST_SIZE)

    feature_indices = [
            header.index(feature)
            for feature in [
                "temperature_2m",
                "dew_point_2m",
                "relative_humidity_2m",
                "surface_pressure",
                "shortwave_radiation",
            ]
        ]
    target_variables = [
        "precipitation_1h",
        "precipitation_6h",
        "precipitation_12h",
        "precipitation_24h",
    ]

    for target_variable in target_variables:
        target_index = header.index(target_variable)

        x_train, y_train = prepare_data(train_data, feature_indices, target_index)
        x_test, y_test = prepare_data(test_data, feature_indices, target_index)

        y_train_transformed = np.log1p(y_train)
        y_test_transformed = np.log1p(y_test)

        model = create_model(len(feature_indices))
        model.fit(x_train, y_train_transformed, epochs=5)
        model.evaluate(x_test, y_test_transformed, verbose=2)

        predictions_transformed = model.predict(x_test)
        predictions = np.expm1(predictions_transformed)
        mse = mean_squared_error(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)
        print(f'Mean Squared Error: {mse}')
        print(f'Mean Absolute Error: {mae}')

        model.save(AI_MODEL_PATH + str(target_variable), save_format='tf')

if __name__ == '__main__':
    main()
