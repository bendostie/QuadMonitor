// code for arduino sensor unit
// see ReadMe for wiring to ESP-01
// error handling not working due to unstable baud rate with ESP-01

//software serial for ESP-01
#include <SoftwareSerial.h>
#include "DHT.h"

//#include "LowPower.h"
SoftwareSerial wifi(3, 2);//RX, TX


//define pins for moisture sensor
#define DHTTYPE DHT11
#define DHTPIN 4 
DHT dht(DHTPIN, DHTTYPE);
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
  delay(5000);
  String Id_m = "111";
  String data_m = String(analogRead(moistOnePin));
  data_m = Id_m + data_m;
  String command_m = "AT+CIPSEND=" + String(data_m.length());
  command_m += "\r\n";
  data_m = data_m + "\r\n";
  wifi.print(command_m);
  delay(1000);
  Serial.print(command_m);
  delay(1000);
  wifi.print(data_m);
  delay(1000);
  Serial.print(data_m);
  Serial.println("after CIP send: " + readWifi());
  
  //humidity
  delay(5000);
  String Id_h = "112";
  String data_h = String(dht.readHumidity());
  data_h = Id_h + data_h;
  String command_h = "AT+CIPSEND=" + String(data_h.length());
  command_h += "\r\n";
  data_h = data_h + "\r\n";
  delay(1000);
  wifi.print(command_h);
  Serial.print(command_h);
  delay(1000);
  wifi.print(data_h);
  Serial.print(data_h);
  Serial.println("after CIP send: " + readWifi());
  
  //temp
  delay(5000);
  String Id_t = "113";
  String data_t = String(dht.readTemperature());
  data_t = Id_t + data_t;
  String command_t = "AT+CIPSEND=" + String(data_t.length());
  command_t += "\r\n";
  data_t = data_t + "\r\n";
  delay(1000);
  wifi.print(command_t);
  Serial.print(command_t);
  delay(1000);
  wifi.print(data_t);
  Serial.print(data_t);
  Serial.println("after CIP send: " + readWifi());
  
  

  delay(5000);
  Serial.println("after data send: " + readWifi());
  
  
  Serial.println(readWifi());
  
  wifi.write("AT+CIPCLOSE\r\n");
  Serial.println("after close: " + readWifi());
  sleep();
  
  //delay(1000);
  

}
