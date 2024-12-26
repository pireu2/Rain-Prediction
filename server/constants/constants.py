import os

# output csv file
API_OUTPUT_FILE = str(os.path.join("server", "data", "data.csv"))
NORMALIZED_DATA = str(os.path.join("server", "data", "data-modified.csv"))

AI_MODEL_PATH = str(os.path.join("server", "models", ""))

# constants for AI training
TEST_SIZE = 0.2
EPOCHS_NUMBER = 5

# normalizing constants
TEMP_N = 40
DEWPOINT_N = 30
HUMIDITY_N = 100
PRESSURE_N = 1010
LUMINOSITY_N = 1000
