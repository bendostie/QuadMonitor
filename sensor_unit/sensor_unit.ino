//software serial for ESP-01
#include <SoftwareSerial.h>
//#include "LowPower.h"
SoftwareSerial wifi(3, 2);//RX, TX


//define pins for moisture sensor
int moistOnePin = A0;
int moistOneValue = 0;
int wifiReset = 8;

//reset wifi

//read wifi message
String readWifi(){
  uint32_t wait = 10000L;
  uint32_t timeStart = millis();
  String result = "";
  int newChar = 10;

  //wait 5 seconds for message
  while ((millis()-timeStart) < wait && !wifi.available());
  while (wifi.available()){
    newChar = wifi.read();
    if (newChar > 13){
      result += (char)newChar;
    }

    
    //Serial.println(wifi.read());
    delay(20);
  }
   return result;
}
void wake(){
  Serial.println("board awake");
  digitalWrite(wifiReset, LOW);
  delay(100);
  Serial.println("wifi reset:");
  digitalWrite(wifiReset, HIGH);
  Serial.println(readWifi());
  delay(60000); //wait for connection to be made
  Serial.println("after wake: " + readWifi()); //clear wifi connection message
}
void sleep(){
  Serial.println("going to sleep");
  wifi.write("AT+GSLP=5000\r\n");
  Serial.println(readWifi());
  //sleep nano
  delay(30000);
}
void checkConnection(){
  Serial.println("checking connection");
  wifi.write("AT+CWJAP?\r\n");
  delay(5000);
  Serial.println("connected to: " + readWifi());
  //make sure ip is ok
}
void connectServer(){
  Serial.println("connecting to server");
  wifi.write("AT+CIPSTART=\"TCP\",\"10.65.1.234\",2001\r\n");
  delay(5000);
  Serial.println("after server connect: " + readWifi());
  
}
void setup() {
  pinMode(wifiReset, OUTPUT);
  Serial.begin(115200);
  wifi.begin(115200);
  
}

void loop() {
  //wake up
  wake();
  //turn off echo
  delay(500);
  wifi.write("ATE0\r\n");
  delay(500);
  Serial.println(readWifi());
  
  //check wifi connection
  checkConnection();
  //establish link to server
  connectServer();
  //read and send value
  String Id = "111";
  String data = String(analogRead(moistOnePin));
  data = Id + data;
  String command = "AT+CIPSEND=" + String(data.length());
  command += "\r\n";
  delay(5000);
  wifi.print(command);
  Serial.print(command);
  delay(5000);
  Serial.println("after CIP send: " + readWifi());
  wifi.print(data);
  delay(5000);
  Serial.println("after data send: " + readWifi());
  
  Serial.print(data);
  Serial.println(readWifi());
  
  wifi.write("AT+CIPCLOSE\r\n");
  Serial.println("after close: " + readWifi());
  sleep();
  
  //delay(1000);
  

}
