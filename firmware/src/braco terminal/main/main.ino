#include "braco.h"
#include "decoder.h"
#include <utility>

braco braco1;

void setup() {
  braco1.attach_pin(13, 12, 15, 2, 18, 19);

  Serial.begin(9600);
  Serial.println("configuracoes prontas");
  
}

void loop() {
  String msg;
  if(Serial.available() > 0){
      while(Serial.available() > 0){
      char c = Serial.read();
      msg = msg + c;
    }
    braco1.comando(msg);
  }
  delay(500);

}
