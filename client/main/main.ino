#include <Wire.h>
#include <Math.h>

#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <Adafruit_TSL2561_U.h>
#include <Adafruit_RGBLCDShield.h>

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#define SEA_LEVEL_RESSURE (1013.25)
#define B_DEWPOINT (17.62)
#define C_DEWPOINT (243.12)

const char *ssid = "DIGI-8ATN";
const char *password = "UmzNDS36";
const char *server = "http://192.168.100.101:5000/predict";

Adafruit_BME280 bme;
Adafruit_TSL2561_Unified tsl = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT, 12345);
Adafruit_RGBLCDShield lcd = Adafruit_RGBLCDShield();

unsigned long delayTime;

struct SensorData
{
    float temperature;
    float pressure;
    float altitude;
    float humidity;
    float luminosity;
    float dewpoint;
};

SensorData sensorData = {0, 0, 0, 0, 0, 0};

void getSensorData();
void configureTSL();
void sendPredictionRequest();

void setup()
{
    Serial.begin(9600);

    lcd.begin(16, 2);
    lcd.print("LCD OK");

    delayTime = 1000;

    bool status;
    status = bme.begin(0x76);
    if (!status)
    {
        Serial.println("Could not find BME280 sensor!");
        while (1)
            ;
    }
    if (!tsl.begin())
    {
        Serial.println("Could not find TSL2561 sensor!");
        while (1)
            ;
    }
    configureTSL();

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        Serial.println("Connecting to WiFi..");
    }
    Serial.println("Connected to the WiFi network");
}

void loop()
{

    uint8_t buttons = lcd.readButtons();
    if (buttons)
    {
        lcd.clear();
        if (buttons & BUTTON_UP)
        {
            getSensorData();
        }
        if (buttons & BUTTON_DOWN)
        {
            sendPredictionRequest();
        }
        if (buttons & BUTTON_SELECT)
        {
            lcd.print("Pressure: ");
            lcd.print(sensorData.pressure);
        }
        if (buttons & BUTTON_LEFT)
        {
            lcd.print("Humidity: ");
            lcd.print(sensorData.humidity);
        }
        if (buttons & BUTTON_RIGHT)
        {
            lcd.print("Luminosity: ");
            lcd.print(sensorData.luminosity);
        }
    }
}

void configureTSL()
{
    tsl.enableAutoRange(true);
    tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_101MS);
}

void getSensorData()
{
    sensorData.temperature = bme.readTemperature();
    sensorData.pressure = bme.readPressure() / 100.0F;
    sensorData.altitude = bme.readAltitude(SEA_LEVEL_RESSURE);
    sensorData.humidity = bme.readHumidity();

    float gamma = (B_DEWPOINT * sensorData.temperature / (C_DEWPOINT + sensorData.temperature)) + log(sensorData.humidity / 100.0);
    sensorData.dewpoint = (C_DEWPOINT * gamma) / (B_DEWPOINT - gamma);

    sensors_event_t event;
    tsl.getEvent(&event);
    if (event.light)
    {
        sensorData.luminosity = event.light;
    }
    else
    {
        sensorData.luminosity = -1;
    }
}

void sendPredictionRequest()
{
    if (WiFi.status() == WL_CONNECTED)
    {
        HTTPClient http;
        http.begin(server);
        http.addHeader("Content-Type", "application/json");

        StaticJsonDocument<200> jsonDoc;
        jsonDoc["temperature"] = sensorData.temperature;
        jsonDoc["humidity"] = sensorData.humidity;
        jsonDoc["pressure"] = sensorData.pressure;
        jsonDoc["luminosity"] = sensorData.luminosity;
        jsonDoc["dewpoint"] = sensorData.dewpoint;
        jsonDoc["prediction_type"] = "ONE_HOUR"; // Change as needed

        String requestBody;
        serializeJson(jsonDoc, requestBody);

        int httpResponseCode = http.POST(requestBody);

        if (httpResponseCode > 0)
        {
            String response = http.getString();
            Serial.println(response);
        }
        else
        {
            Serial.print("Error on sending POST: ");
            Serial.println(httpResponseCode);
        }

        http.end();
    }
    else
    {
        Serial.println("WiFi Disconnected");
    }
}
