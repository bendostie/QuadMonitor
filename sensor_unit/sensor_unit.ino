//software serial for ESP-01
#include <SoftwareSerial.h>
SoftwareSerial wifi(3, 2);//RX, TX


//define pins for moisture sensor
int moistOnePin = A0;
int moistOneValue = 0;
int wifiReset = 8;


//read wifi message
String readWifi(){
  uint32_t wait = 5000L;
  uint32_t timeStart = millis();
  String result = "";
  int newChar = 10;

  //wait 5 seconds for message
  while ((millis()-timeStart) < wait);
  while (wifi.available()){
    newChar = wifi.read();
    if ((newChar != 13) && (newChar !=10)){
      result += newChar;
    }
    
    //Serial.println(wifi.read());
    //delay(20);
  }
   return result;
}
void setup() {
  
  pinMode(wifiReset, OUTPUT);
  Serial.begin(9600);
  wifi.begin(115200);
}

void loop() {
  //check wifi connection
  //turn off echo
  //wifi.write("ATE0\r\n");
  
  
  digitalWrite(wifiReset, LOW);
  delay(100);
  digitalWrite(wifiReset, HIGH);
  Serial.println(readWifi());
  
  delay(7000);

    
  //moistOneValue = analogRead(moistOnePin);
  //Serial.println(moistOneValue);
  //delay(1000);
  

}
