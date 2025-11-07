#include <ESP32Servo.h>
int num;
int pos = 90;
Servo servo1;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Hello, ESP32!");
  servo1.attach(2);
}

void loop() {
  if(Serial.available() > 0){
    num = Serial.parseInt();
    if(pos < num){
      for(int i = pos; i <= num; i++)
      {
        servo1.write(i);
        delay(15);
        Serial.print(i);
      }
    }
    else{
      for(int i = pos; i >= num; i--)
      {
        servo1.write(i);
        delay(15);
        Serial.print(i);
      }
    }
    
    pos = num;
    while(Serial.available() > 0){
      Serial.read();
    }
  }

  Serial.println(pos);
  delay(700);
}