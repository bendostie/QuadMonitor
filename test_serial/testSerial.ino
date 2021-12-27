// code for testing ESP-01
// forwards serial through arduino
// see ReadMe for wiring diagram
// baud rate with ESP-01 and software serial unstable

#include <SoftwareSerial.h>
SoftwareSerial myESP(3, 2);//RX, TX

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  myESP.begin(115200);
  myESP.write("AT\r\n");
}

  // put your main code here, to run repeatedly:
void loop() {
  
  while(Serial.available() > 0) {
     myESP.write(Serial.read());
  }
  while(myESP.available() > 0) {
     Serial.write(myESP.read());
     delay(20);
  }
}
