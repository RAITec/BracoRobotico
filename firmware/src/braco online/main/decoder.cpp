
#include "decoder.h"
#include <utility>


std::pair<int, int> decoder::descript(String msg){
    int num_servo = get_servo(msg);
    int angulo = get_ang(msg, num_servo);

    std::pair<int, int> comand;
    comand = std::make_pair(num_servo, angulo);
    return comand;
}




int decoder::get_ang(String frase, int num_servo){
  unsigned int i = 0; // percorrer a frase
    bool verif = 0; //verificação se o angulo foi passado
    int valor = 0; //valor do angulo

    //chegando no numero após os ::
    while(frase[i] != ':' && i < frase.length()){
      i++;
    }
    i++;

    if(num_servo == 5 && frase[i] == 'O') return 0;
    else if(num_servo == 5 && frase[i] == 'C') return 1;
    
    //tranformando
    while (frase[i] >= '0' && frase[i] <= '9' && i < frase.length())
    {
        valor = valor * 10; // multiplicando por 10 para somar com o proximo(apos a primeira iteração)
        valor = valor + (frase[i] - '0'); // tranformando um char em um int
        verif = 1;
        i++;
    }


    if(verif == 0){
        return -1; //erro 
    } 
    return valor;
    
}


int decoder::get_servo(String frase){
  if(frase[0] == 'G'){
    return 5;
  }

  unsigned int i = 0;
    int valor = 0;
    bool verif = 0;

    //pegando o numero antes do :
    while((frase[i] < '0' || frase[i] > '9') && frase[i] != ':' && i < frase.length()){ 
        i++;
    }
    
    //tranformando em inteiro
    while (frase[i] >= '0' && frase[i] <= '9' && i < frase.length())
    {
        valor = valor * 10; // multiplicando por 10 para somar com o proximo(apos a primeira iteração)
        valor = valor + (frase[i] - '0'); // tranformando um char em um int
        verif = 1;
        i++;
    }
    valor--;

    if(verif == 0 || !(valor <= 4 && valor >= 0)){
        return -1; //erro 
    } 
    return valor;

}

/*
//pegar o angulo do servo
int pars_int_angulo(String frase){
    unsigned int i = 0; // percorrer a frase
    bool verif = 0; //verificação se o angulo foi passado
    int valor = 0; //valor do angulo

    //chegando no numero após os ::
    while(frase[i] != ':' && i < frase.length()){
      i++;
    }
    i++;
    
    //tranformando
    while (frase[i] >= '0' && frase[i] <= '9' && i < frase.length())
    {
        valor = valor * 10; // multiplicando por 10 para somar com o proximo(apos a primeira iteração)
        valor = valor + (frase[i] - '0'); // tranformando um char em um int
        verif = 1;
        i++;
    }


    if(verif == 0){
        return -1; //erro 
    } 
    return valor;
    
}
*/


/*



//pegar o numero do servo
int pars_int_servo(string frase){
    unsigned int i = 0;
    int valor = 0;
    bool verif = 0;

    //pegando o numero antes do :
    while((frase[i] < '0' || frase[i] > '9') && frase[i] != ':' && i < frase.length()){ 
        i++;
    }
    
    //tranformando em inteiro
    while (frase[i] >= '0' && frase[i] <= '9' && i < frase.length())
    {
         if(verif == 1){
            valor = valor * 10; // multiplicando por 10 para somar com o proximo(apos a primeira iteração)
        }
        valor = valor + (frase[i] - '0'); // tranformando um char em um int
        verif = 1;
        i++;
    }

    if(verif == 0){
        return -1; //erro 
    } 
    return valor;
    
}*/