#include <WiFi.h>
#include <PubSubClient.h>

#include "braco.h"
#include "decoder.h"
#include <utility>

// --- Configurações da Rede e MQTT ---
// Altere estes valores para os da sua rede
const char* ssid = "RAITEC - LATIN 2.4G"; // Nome da rede wifi
const char* password = "Raitecos$2026"; // Senha da rede wifi
const char* mqtt_server = "192.168.1.118"; // IP do seu servidor MQTT local
const int mqtt_port = 1883;
const char* MQTT_TOPIC = "braco/comando"; // Tópico a ser enviado as mensagens
const char* username = "natan"; // Nome de usuário do servidor local
const char* passwordServer = "123456"; // Senha do servidor local


//iniciando braço
braco braco1;

// --- Cliente WiFi e MQTT ---
// Usamos WiFiClient para conexões inseguras (sem SSL/TLS)
WiFiClient wifiClient;
PubSubClient client(wifiClient);

// --- Variáveis para Publicação Temporizada ---
unsigned long lastMsg = 0;
long value = 0;
const int MSG_BUFFER_SIZE = 50;
char msg[MSG_BUFFER_SIZE];

// --- Protótipos de Funções ---
void setup_wifi();
void reconnect();
void mqttCallback(char* topic, byte* payload, unsigned int length);


void setup() {
  Serial.begin(115200);
  delay(100);

  //inicializando
  braco1.attach_pin(2, 12, 13, 15, 18, 19);
   delay(100);

  setup_wifi(); // Conecta ao Wi-Fi

  // Configura o servidor e a porta MQTT
  client.setServer(mqtt_server, mqtt_port);
  // Define a função que será chamada ao receber uma mensagem
  client.setCallback(mqttCallback);
}

void loop() {
  // Se não estiver conectado, tenta reconectar
  if (!client.connected()) {
    reconnect();
  }
  // Mantém a conexão MQTT ativa e processa mensagens recebidas
  client.loop();

  // Lógica para enviar uma mensagem a cada 2 segundos (não bloqueante)
  
}

// Função para conectar ao Wi-Fi
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando-se a ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  // Espera a conexão ser estabelecida
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi conectado!");
  Serial.print("Endereço IP: ");
  Serial.println(WiFi.localIP());
}

// Função chamada quando uma mensagem MQTT é recebida
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Mensagem recebida no tópico [");
  Serial.print(topic);
  Serial.print("]: ");
  
  String msg;
 
  //obtem a string do payload recebido
  for(int i = 0; i < length; i++) 
  {
    char c = (char)payload[i];
    Serial.print(c);
    msg += c;
  }
  Serial.println();
  if (length > 0) {
    delay(100);
    braco1.comando(msg);
  }
  delay(1000);
}




// Função para reconectar ao servidor MQTT
void reconnect() {
  // Loop até que a reconexão seja bem-sucedida
  while (!client.connected()) {
    Serial.print("Tentando conexão MQTT...");
    
    // Cria um ID de cliente aleatório
    String clientId = "ESP32Client-" + String(random(0xffff), HEX);
    
    // Tenta conectar com usuário e senha (se não precisar, deixe as strings vazias "")
    if (client.connect(clientId.c_str(), username, passwordServer)) {
      Serial.println("conectado!");
      
      // Publica uma mensagem de "boas-vindas" e se inscreve no tópico de interesse
      //client.publish(MQTT_TOPIC, "ESP32 conectado");
      client.subscribe(MQTT_TOPIC);
    } else {
      Serial.print("falhou, rc=");
      Serial.print(client.state());
      Serial.println(" | tentando novamente em 5 segundos");
      delay(5000); // Espera 5 segundos antes de tentar novamente
    }
  }
}