#include "braco.h"
#include <ServoEasing.hpp>
#include <utility>
#include "decoder.h"

ServoEasing servo[6];
std::pair<int, int> limites[6];
/*
limites
garra(5) - 30 até 90
servo 4 - 0 a 180
servo 3 - 0 a 180
servo 2 - problema
servo 1 - 20 a 180
servo 0 - 0 a 180
*/
void braco::attach_pin(int pin0, int pin1, int pin2, int pin3, int pin4, int pin5){

  //configurando servo 0
  servo[0].attach(pin0);
  servo[0].setEasingType(EASE_SINE_IN_OUT);
  servo[0].setSpeed(90);
  limites[0] = std::make_pair(0, 180);

  //configurando servo 1
  servo[1].attach(pin1);
  servo[1].setEasingType(EASE_SINE_IN_OUT);
  servo[1].setSpeed(90);
  limites[1] = std::make_pair(15, 180);

  //configurando servo 2 - problema
  servo[2].attach(pin2);
  servo[2].setEasingType(EASE_SINE_IN_OUT);
  servo[2].setSpeed(90);
  limites[2] = std::make_pair(0, 180);

  //configurando servo 3
  servo[3].attach(pin3);
  servo[3].setEasingType(EASE_SINE_IN_OUT);
  servo[3].setSpeed(90);
  limites[3] = std::make_pair(0, 180);

  //configurando servo 4
  servo[4].attach(pin4);
  servo[4].setEasingType(EASE_SINE_IN_OUT);
  servo[4].setSpeed(90);
  limites[4] = std::make_pair(0, 180);

  //configurando servo 5
  servo[5].attach(pin5);
  servo[5].setEasingType(EASE_SINE_IN_OUT);
  servo[5].setSpeed(90);
  limites[5] = std::make_pair(30, 100);



}




int braco::get_posicao(int num_servo){

  return servo[num_servo].getCurrentAngle();
}

void braco::exec_comand(int num_servo, int angulo){
  Serial.print("iniciar movimento \nservo ");
  Serial.print(num_servo);
  Serial.print(": ");
  Serial.print(this->get_posicao(num_servo));
  Serial.print(" -> ");
  servo[num_servo].easeTo(angulo);
  Serial.println(this->get_posicao(num_servo));
  Serial.println("movimento concluido\n");

}


int braco::limite(int num_servo, int angulo){

  if(angulo > limites[num_servo].second){
    return limites[num_servo].second;
  }
  else if(angulo < limites[num_servo].first){
    return limites[num_servo].first;
  }
  return angulo;

}

int braco::garra(int num_servo, int angulo){
  if(num_servo != 5) return angulo;
  if(angulo == 1) return this->get_posicao(num_servo) + 25;
  return this->get_posicao(num_servo) - 25;
}

void braco::comando(String msg){
  std::pair<int, int> comando = decoder::descript(msg);
  if( comando.first == -1 || comando.second == -1 ){
    Serial.println("mensagem invalida");
    return;
  }
  comando.second = this->garra(comando.first, comando.second);
  comando.second = this->limite(comando.first, comando.second);
  this->exec_comand(comando.first, comando.second);

  this->posicao_geral();
 }


void braco::posicao_geral(){
  for(int i = 0; i < 6; i++){
    Serial.print("servo ");
    Serial.print(i);
    Serial.print(":");
    Serial.println(this->get_posicao(i));
  }
}





