#include <WiFi.h>
#include <WiFiUdp.h>

// ===== CONFIGURACIÓN =====
const char* ssid = "INFINITUMC3DD_2.4";
const char* password = "5RxAGM8u4m";

// IP del receptor (PC o celular)
const char* receiverIP = "192.168.1.107";
const int receiverPort = 5005;

// Intervalo entre paquetes (ms)
const unsigned long SEND_INTERVAL = 100;

// =========================
WiFiUDP udp;
unsigned long packetCount = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);

  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConectado!");
  Serial.print("IP ESP32: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  unsigned long now = millis();

  // Payload: contador + timestamp
  char payload[64];
  snprintf(payload, sizeof(payload), "%lu,%lu", packetCount, now);

  udp.beginPacket(receiverIP, receiverPort);
  udp.write((uint8_t*)payload, strlen(payload));
  udp.endPacket();

  packetCount++;

  delay(SEND_INTERVAL);
}
