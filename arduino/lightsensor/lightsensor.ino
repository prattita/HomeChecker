const int LIGHT_SENSOR_PIN = A0;
const String NAME = "light1";

void setup() {
  pinMode(LIGHT_SENSOR_PIN, INPUT);
  Serial.begin(19200);
}

void loop() {
  int start = millis();
  Serial.print("[{\"sensor\": \"");
  Serial.print(NAME);
  Serial.print("\", \"light_level\": ");
  Serial.print(analogRead(LIGHT_SENSOR_PIN));
  Serial.println("}]");
  Serial.flush();
  while( millis() < start + 1000 ) {
    // wait until done
  }
}
