#include "config.h"
#include <WiFi.h>
int sensorPin = 34;
volatile long pulse;
unsigned int pulseTotal = 0;
volatile long pulseC;
volatile long treshold = 5;

void setup() {
  pinMode(sensorPin, INPUT);
  Serial.begin(9600);

  Serial.println();
  Serial.println("******************************************************");
  Serial.print("Connecting to ");
  Serial.println(MY_WIFI_SSID);
  WiFi.begin(MY_WIFI_SSID, MY_WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  
  attachInterrupt(digitalPinToInterrupt(sensorPin), increase, RISING);
}

void req(int state, volatile long rate) {
  WiFiClient client;
  String footer = String(" HTTP/1.1\r\n") + "Host: " + String(T_HOST) + "\r\n" + "Connection: close\r\n\r\n";
  if (!client.connect(T_HOST, T_PORT)) {
    return;
  }
  client.print("GET /water/" + String(state) + "/" + String(rate) + footer);
}

void loop() {
  while(true) {
    pulseC = rar();
    Serial.println(pulseC);
    if (pulseC > treshold) {
      Serial.println("S1: Water detected!");
      req(1, 0);
      delay(1000);
      break;
    }
    req(2, 0);
    Serial.println("S1: Water NOT detected!");
    delay(1000);
  }

  while(true) {
    pulseC = rar();
    Serial.println(pulseC);
    if (pulseC > treshold) {
      req(2, 0);
      Serial.println("S2: Water detected!");
      delay(1000);
    } else {
      Serial.println("S2: Water NOT detected!");
      req(0, pulseTotal);
      pulseTotal = 0;
      delay(1000);
      break;
    }
  }
}
void increase() {
  pulse++;
}

long rar() {
  volatile long p = pulse;
  pulse = 0;
  pulseTotal = pulseTotal + p;
  return p;
}
