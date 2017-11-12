#include <CurieBLE.h>

const int LIGHT_SENSOR_PIN = A0;
const String NAME = "demoPi";

void setup() {
  pinMode(LIGHT_SENSOR_PIN, INPUT);
  Serial.begin(9600);
}

void loop() {
  Serial.print("[{\"sensor\": \"");
  Serial.print(NAME);
  Serial.print("\", \"light_level\": ");
  Serial.print(getAvgLightLevel(1000));
  Serial.println("}]");
//  Serial.println(millis());
}

int getAvgLightLevel(int duration) {
  unsigned long int sum;
  int del = duration / 30;
  for (int i=0; i<30; i++) {
    sum += analogRead(LIGHT_SENSOR_PIN);
    delay(del);
  }
  return sum / 30;
}

