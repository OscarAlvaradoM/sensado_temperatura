#include "max6675.h"

int thermoDO = 19;
int thermoCS = 23;
int thermoCLK = 5;

int LED_BUILTIN = 2;

MAX6675 thermocouple(thermoCLK, thermoCS, thermoDO);

unsigned long t0;

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);

  delay(500); // estabilizar sensor
  t0 = millis();

  // Encabezado CSV
  Serial.println("tiempo_s,temperatura_C");
}

void loop() {
  unsigned long t = millis() - t0;
  float tiempo = t / 1000.0;
  float T = thermocouple.readCelsius();

  Serial.print(tiempo);
  Serial.print(",");
  Serial.println(T);

  digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  delay(500); // >= 250 ms
}
