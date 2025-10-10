#include <ArduinoJson.h>
#include <ArduinoJson.hpp>

int pins[] = {10, 11, 12, 13};
const int numOfPins = sizeof(pins) / sizeof(pins[0]);
bool availablePins[numOfPins];

void setup() {
  // put your setup code here, to run once:
  for (int i = 0; i < numOfPins; i++) {
    pinMode(pins[i], OUTPUT);
    availablePins[i] = false;
  }
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

  if (Serial.available()) {

    char command = Serial.read();
    
    if (command == 'A') {

      StaticJsonDocument<128> doc;
      JsonArray arr = doc.createNestedArray("available_pins");

      for (int i = 0; i < numOfPins; i++) {
        if (!availablePins[i]) {
          arr.add(pins[i]);    
        }
      }

      serializeJson(doc, Serial);
      Serial.println();

    } else if (command == 'C') {

      int chosenPin = Serial.parseInt();

      for (int i = 0; i < numOfPins; i++) {

        if (pins[i] == chosenPin) {
          availablePins[i] = true;
          digitalWrite(chosenPin, HIGH);
        }

      }

    } else if (command == 'B') {

      StaticJsonDocument<128> doc;
      JsonArray reservedPins = doc.createNestedArray("reserved_pins");

      for (int i = 0; i < numOfPins; i++) {

        if (availablePins[i] == true) {

          reservedPins.add(pins[i]);

        }

      }

      serializeJson(doc, Serial);
      Serial.println();

    } else if (command == 'O') {  

      int chosenPin = Serial.parseInt();

      for (int i = 0; i < numOfPins; i++) {

        if (pins[i] == chosenPin) {

          availablePins[i] = false;
          digitalWrite(chosenPin, LOW);

        }

      }

    } else if (command == 'U') {

      String s = Serial.readStringUntil('\n');
      s.substring(1);
      StaticJsonDocument<128> doc;
      deserializeJson(doc, s);

      int size = doc.size();

      for (int k = 0; k < numOfPins; k++) availablePins[k] = false;

      for (int i = 0 ; i < size; i++) {
        for (int j = 0; j < numOfPins; j++) {
        
          if (doc[i] == pins[j]) {
            availablePins[j] = true;
          }

        }
      }


    }
  }

}
