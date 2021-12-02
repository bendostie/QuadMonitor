#include <SoftwareSerial.h>
SoftwareSerial myESP(3, 2);//RX, TX

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
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
