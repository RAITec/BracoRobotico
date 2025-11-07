 README: Classe para a movimentação do braço

Este documento detalha o funcionamento e o método da classe criada para a ESP32 com o objetivo de implemntar a lógica de movimento do braço roótico com comando de voz



## Links e Referências

### Sobre ServoEasing

  * [Github - ServoEasing](https://github.com/ArminJo/ServoEasing/tree/master)

### intalando arduino IDE
  * [tutorial de instalção e uso do Arduino IDE](https://www.electronicwings.com/esp32/getting-started-with-esp32)

### Tutorial para programação orientada a objetos em Arduino IDE

  * [documentação tutorial com uma clase de Leds](https://roboticsbackend.com/arduino-object-oriented-programming-oop/)
  * [Video explicativo de classes em arduino IDE](https://www.youtube.com/watch?v=aye91fDCF9g)

## Introdução

O projeto do Braço Robótico é controlado pela ESP32, um microcontrolador, que irá receber mensagens de um reconhecedor de voz a partir de uma comunicação por wifi.

nessa documentação, focaremos no código voltado para a lógica de movimento do braço robótico pela ESP32, a partir de um modelo de mensagem do reconhecedor.

## Requisitos do projeto

   * Arduino IDE baixado e configurado para ESP32 (com um tutorial acima).
   * Biblioteca ServoEasing para movimentos de servo Motor (detalhada na classe braco).
   * Modelo padrão de mensagem (detalhado na classe decoder)
   * ter os arquivos, braco.h, braco.cpp, decoder.h, decoder.cpp, no mesmo sketch do projeto.


## Funcionalidades

Para o Projeto, teremos ao todo três partes que se interconectam. 

1.  **main**
2.  **classe braco**
3.  **classe decoder**

o fluxo de funcionamento segue:
main - como usar a classe.
classe braco - funções implementadas na classe.
decoder - como descriptografar a mensagem do reconhecedor.

### 1\. main (utilização do projeto)

Na primeira parte, descrevemos como usar as classes para um usuario que queira implementar em seu projeto.
nessa parte, precisaremos de incluir o arquivo da classe braco, usando:
```Cpp
   #include "braco.h";
```

Depois, instanciamos um objeto da classe braco, no escopo geral do código:
```Cpp
   braco braco1;
```

Em seguida, ativaremos os pinos dos servos na função setup. Da esquerda para a direira, segue a sequencia dos pinos usados para o servo 1, 2, 3, 4, 5, 6:
```Cpp
   braco1.attach_pin(pin_1, pin_2, pin_3, pin_4, pin_5, pin_6);
```
Atenção: o Pino 6 serve para a garra, então terá uma lógica diferente dos demais.

Por ultimo, só precisamos passar a mensagem sempre que quisermos mover o braco, usando:
```Cpp
   braco1.comando(msg);
```
Com msg sendo a string da mensagem.

Segure um exemplo de utilização da classe braco, utilizando o terminal para fins didáticos, mas seu uso envolve qualquer aplicação contanto que a mensagem siga o modelo:


**Exemplo de Uso:**

```Cpp
//bibliotecas
#include "braco.h"
#include <utility>

//instanciando braco
braco braco1;

void setup() {
    //inicializando pinos dos servos
  braco1.attach_pin(13, 12, 15, 2, 18, 19);

    //inicializando terminal Serial
  Serial.begin(9600);
  Serial.println("configuracoes prontas");
  
}

void loop() {
    //msg em formato string
  String msg;
  if(Serial.available() > 0){

    //leitura da mensagem pelo terminal
      while(Serial.available() > 0){
      char c = Serial.read();
      msg = msg + c;
    }
    //comando para o braco
    braco1.comando(msg);
  }
  delay(500);
}
```

**Observação:** Para que o projeto funcione, é necessário ter os arquivos, braco.h, braco.cpp, decoder.h, decoder.cpp, no mesmo sketch do projeto.

### 2\. classe decoder (Decodificação de mensagens)

Essa é uma classe estática, ou seja, sem instanciação. Ela srvirar para pegarmos uma mensagem em string e convertermos para dois numeros que queremos, o servo que se movimentará. segue as explicações das mensagens de entrada e saída:

**tipo de entrada esperada:**

A classe decoder espera um tipo padrão de mensagem. Para os servos 1 a 5, que tem maiores graus de liberdade, vamos ter a seguinte estrutura
   * Servo[servo]:[angulo]

Em que 
   * "[servo]" - numero maior ou igual a 1 e menor ou igual a 5, como 1, 2, 3, 4, 5, simboliza o servo a ser mexido;
   * "[angulo]" - numero  multiplo de 5 entre 5 e 180, como 5, 25, 130, simboliza o angulo a ser movido;
   * Ex: Servo4:40

Para o servo 6, da garra, temos a seguinte estrutura:
   * GARRA:[comando]

Em que:
   * [Comando] - "OPEN", para abrir, ou "CLOSE", para fechar.
   * Ex: GARRA:OPEN

**tipo de saída esperada:**

A classe decoder, retornará um dado pair de dois inteiros, em que 
   * first - numero do servo.
   * seconde - comando para o servo.


### 3\. classe braco (lógica de movimento)

A classe braco irá comandar o ciclo de movimento do braço. Ela primeiro obtem a string da main, depois manda essa string para a decoder e recebe o comando.
Com o comando, o braco usa a classe ServoEasing para comandar os servos motores. Essa classe serve para suavizar o movimento de servos, controlando sua velocidade automaticamente.

As seguintes funções referen-se as funções da classe braco:


```Cpp
    void attach_pin(int pin0, int pin1, int pin2, int pin3, int pin4, int pin5); //definir os pinos dos servos
    int get_posicao(int num_servo); //retornar a posição do servo
    void exec_comand(int num_servo, int angulo); //executar o comando dado pelo decodificador
    int limite(int num_servo, int angulo); // defini limites para o braço
    void comando(String msg); //comandar o braço, manda a mensagem para o decoder e o comando para a execução
    int garra(int num_servo, int angulo); //logica diferente de movimento para a garra
    void posicao_geral(); // printa a posição de todos os servos
```

A principal funcionalidade diferente, fora os servos normais, é o controle de limites, em que o usuàrio pode colocar limites no vetor de pairs inteiros "limites[]". nesse caso, o angulo fornecido não pode utrapassar o limite definido pelo usuário, o que é necessário para a parte fisica do braço, quando alguns servos só podem ir até certo angulo. Um servo que usa isso é o da garra. ele está situado em uma faixa possivel de angulo de 60 graus [10, 70]. Caso passe dessa faça, ele tende a forçar o servo, estando sujeito a danificações.