import os

# addresses for the sensors
BME280_ADDRESS = 0x76
TSL2561_ADDRESS = 0x39

# output csv file
API_OUTPUT_FILE = str(os.path.join("data", "data.csv"))
MODIFIED_OUTPUT_FILE = str(os.path.join("data", "data-modified.csv"))

# constant for computing dewpoint
B_DEWPOINT = 17.62
C_DEWPOINT = 243.12

TEST_SIZE = 0.4
