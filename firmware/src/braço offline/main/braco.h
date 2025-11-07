
#ifndef BRACO_H
#define BRACO_H
#include <Arduino.h>
#include <utility>

class braco{
  
  public:
    void attach_pin(int pin0, int pin1, int pin2, int pin3, int pin4, int pin5);
    int get_posicao(int num_servo);
    void exec_comand(int num_servo, int angulo);
    int limite(int num_servo, int angulo);
    void comando(String msg);
    int garra(int num_servo, int angulo);
    void posicao_geral();
};


#endif