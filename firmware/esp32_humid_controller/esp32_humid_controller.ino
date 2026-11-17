// CoSE Mycoponic MVP — ESP32 Humidity & Air Pump Controller
// Reads an SHT31/SHT30 I2C temp/humidity sensor hung through the 10 mm
// lid port (120 deg) and regulates the external air pump via GPIO 25.

#include <Wire.h>
#include "Adafruit_SHT31.h"

static constexpr uint8_t PIN_SDA = 21;
static constexpr uint8_t PIN_SCL = 22;
static constexpr uint8_t PIN_PUMP_RELAY = 25;

static constexpr float RH_TARGET_LOW  = 85.0f;  // Turn pump ON below 85% RH
static constexpr float RH_TARGET_HIGH = 90.0f;  // Turn pump OFF at/above 90% RH
static constexpr unsigned long SAMPLE_MS = 2000;
static constexpr unsigned long MAX_PUMP_ON_MS = 120000; // 2 min safety cap

Adafruit_SHT31 sht31 = Adafruit_SHT31();
bool pumpOn = false;
unsigned long pumpStartMs = 0;

void setPump(bool on) {
  pumpOn = on;
  digitalWrite(PIN_PUMP_RELAY, on ? HIGH : LOW);
  if (on) pumpStartMs = millis();
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_PUMP_RELAY, OUTPUT);
  setPump(false);
  Wire.begin(PIN_SDA, PIN_SCL);
  if (!sht31.begin(0x44)) {
    Serial.println("ERROR: SHT31/SHT30 not found at 0x44");
  }
}

void loop() {
  float t = sht31.readTemperature();
  float rh = sht31.readHumidity();

  if (isnan(t) || isnan(rh)) {
    Serial.println("WARN: Sensor read failed — pump OFF");
    setPump(false);
  } else {
    Serial.printf("T=%.2f C | RH=%.1f%% | Pump=%s\n", t, rh, pumpOn ? "ON" : "OFF");
    if (!pumpOn && rh < RH_TARGET_LOW) {
      setPump(true);
    } else if (pumpOn && (rh >= RH_TARGET_HIGH || (millis() - pumpStartMs > MAX_PUMP_ON_MS))) {
      setPump(false);
    }
  }
  delay(SAMPLE_MS);
}
