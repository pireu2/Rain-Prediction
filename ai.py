import csv
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from constants.constants import MODIFIED_OUTPUT_FILE, TEST_SIZE

with open(MODIFIED_OUTPUT_FILE, "r") as file:
    reader = csv.DictReader(file)
    header = list(next(reader))
    data = [list(row.values()) for row in reader]


train_data, test_data = train_test_split(data, test_size=TEST_SIZE)
model = KNeighborsRegressor(n_neighbors=100)

target_variables = [
    "precipitation_1h",
    "precipitation_6h",
    "precipitation_12h",
    "precipitation_24h",
]

for target_variable in target_variables:
    target_index = header.index(target_variable)
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
    x_train = [[float(row[i]) for i in feature_indices] for row in train_data]
    y_train = [float(row[target_index]) for row in train_data]

    x_test = [[float(row[i]) for i in feature_indices] for row in test_data]
    y_test = [float(row[target_index]) for row in test_data]

    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    mse = mean_squared_error(y_test, predictions)
    print(f'Mean squared error for {target_variable}: {mse}')
