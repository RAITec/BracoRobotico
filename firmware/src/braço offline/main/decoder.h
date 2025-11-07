#ifndef DECODER_H
#define DECODER_H
#include <Arduino.h>
#include <utility>

class decoder{
  
  public:
    static std::pair<int, int>  descript(String msg);
    static int get_servo(String frase);
    static int get_ang(String frase, int num_servo);
};


#endif