#include <math.h>

/* This doesn't work, even though it's Grove's example code for the thing.
 *  Rather tan waste time, we'll add a simulation.
 */


const int TEMP_SENSOR_PIN = A0;
const String NAME = "temp1";

void setup() {
  pinMode(TEMP_SENSOR_PIN, INPUT);
  Serial.begin(19200);
}

void loop() {
  start = millis();
  Serial.print("[{\"sensor\": \"");
  Serial.print(NAME);
  Serial.print("\", \"temp_level\": ");
  Serial.print(getTemperature());
  Serial.println("}]");
  Serial.flush();
  while (millis() < start + 1000) {
    // wait until this loop has taken 1 second
  }
}

float getTemperature() {
  static int B=3975;                  //B value of the thermistor
  int a=analogRead(TEMP_SENSOR_PIN);
  float resistance=(float)(1023-a)*10000/a; //get the resistance of the sensor
  return 1/(log(resistance/10000)/B+1/298.15)-273.15; //convert to temperature via datasheet
}
