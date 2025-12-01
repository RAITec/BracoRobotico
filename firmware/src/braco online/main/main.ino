#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <time.h>
#include "braco.h"
#include "decoder.h"
#include <utility>

// É NECESSÁRIO MUDAR O CERTIFICADO A DEPENDER DO SERVER UTILIZADO! USAR TLS É UM SACO
static const char ROOT_CA_PEM[]= R"EOF(
-----BEGIN CERTIFICATE-----
MIIEAzCCAuugAwIBAgIUBY1hlCGvdj4NhBXkZ/uLUZNILAwwDQYJKoZIhvcNAQEL
BQAwgZAxCzAJBgNVBAYTAkdCMRcwFQYDVQQIDA5Vbml0ZWQgS2luZ2RvbTEOMAwG
A1UEBwwFRGVyYnkxEjAQBgNVBAoMCU1vc3F1aXR0bzELMAkGA1UECwwCQ0ExFjAU
BgNVBAMMDW1vc3F1aXR0by5vcmcxHzAdBgkqhkiG9w0BCQEWEHJvZ2VyQGF0Y2hv
by5vcmcwHhcNMjAwNjA5MTEwNjM5WhcNMzAwNjA3MTEwNjM5WjCBkDELMAkGA1UE
BhMCR0IxFzAVBgNVBAgMDlVuaXRlZCBLaW5nZG9tMQ4wDAYDVQQHDAVEZXJieTES
MBAGA1UECgwJTW9zcXVpdHRvMQswCQYDVQQLDAJDQTEWMBQGA1UEAwwNbW9zcXVp
dHRvLm9yZzEfMB0GCSqGSIb3DQEJARYQcm9nZXJAYXRjaG9vLm9yZzCCASIwDQYJ
KoZIhvcNAQEBBQADggEPADCCAQoCggEBAME0HKmIzfTOwkKLT3THHe+ObdizamPg
UZmD64Tf3zJdNeYGYn4CEXbyP6fy3tWc8S2boW6dzrH8SdFf9uo320GJA9B7U1FW
Te3xda/Lm3JFfaHjkWw7jBwcauQZjpGINHapHRlpiCZsquAthOgxW9SgDgYlGzEA
s06pkEFiMw+qDfLo/sxFKB6vQlFekMeCymjLCbNwPJyqyhFmPWwio/PDMruBTzPH
3cioBnrJWKXc3OjXdLGFJOfj7pP0j/dr2LH72eSvv3PQQFl90CZPFhrCUcRHSSxo
E6yjGOdnz7f6PveLIB574kQORwt8ePn0yidrTC1ictikED3nHYhMUOUCAwEAAaNT
MFEwHQYDVR0OBBYEFPVV6xBUFPiGKDyo5V3+Hbh4N9YSMB8GA1UdIwQYMBaAFPVV
6xBUFPiGKDyo5V3+Hbh4N9YSMA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQEL
BQADggEBAGa9kS21N70ThM6/Hj9D7mbVxKLBjVWe2TPsGfbl3rEDfZ+OKRZ2j6AC
6r7jb4TZO3dzF2p6dgbrlU71Y/4K0TdzIjRj3cQ3KSm41JvUQ0hZ/c04iGDg/xWf
+pp58nfPAYwuerruPNWmlStWAXf0UTqRtg4hQDWBuUFDJTuWuuBvEXudz74eh/wK
sMwfu1HFvjy5Z0iMDU8PUDepjVolOCue9ashlS4EB5IECdSR2TItnAIiIwimx839
LdUdRudafMu5T5Xma182OC0/u/xRlEm+tvKGGmfFcN0piqVl8OrSPBgIlb+1IKJE
m/XriWr/Cq4h/JfB7NTsezVslgkBaoU=
-----END CERTIFICATE-----
)EOF";


//configurando servo
braco braco1;

const char* ssid = "wifi_ssid"; // mudar
const char* password = "wifi_password"; // mudar
const char* mqtt_server = "test.mosquitto.org";
const int mqtt_port = 8883;

WiFiClientSecure secureClient;
PubSubClient client(secureClient);

// Configuração NTP
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = -3 * 3600;           // Não mexa
const int   daylightOffset_sec = 0;       

unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE  (500)
char msg[MSG_BUFFER_SIZE];
int value = 0;

void setup() {
  Serial.begin(115200);
  delay(100);

  //inicializando braço
  braco1.attach_pin(13, 2, 12, 18, 15, 19);

  // Conexão com WiFi
  Serial.printf("Conectando a %s", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print('.');
  }
  Serial.println("\nWiFi conectado");
  Serial.print("IP addr: ");
  Serial.println(WiFi.localIP());

  // Configuração de hora via NTP
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  Serial.print("Esperando sincronização NTP");
  time_t now = time(nullptr);
  unsigned long tstart = millis();
  while (now < 1600000000 && millis() - tstart < 20000) { // espera até timestamp razoável ou 20s timeout
    Serial.print(".");
    delay(500);
    now = time(nullptr);
  }
  Serial.println();
  if (now < 1600000000) {
    Serial.println("Aviso: hora NTP não sincronizada (timeout). A validação do certificado pode falhar.");
  } else {
    struct tm timeinfo;
    gmtime_r(&now, &timeinfo);
    Serial.printf("Hora atual: %s", asctime(&timeinfo));
  }


  secureClient.setCACert(ROOT_CA_PEM);
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(mqttCallback);
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  Serial.printf("Mensagem recebida [%s]: ", topic);
  String msg;
 
  //obtem a string do payload recebido
  for(int i = 0; i < length; i++) 
  {
    char c = (char)payload[i];
    msg += c;
  }
  
  if (length > 0) {
    delay(100);
    braco1.comando(msg);
  }
  delay(1000);
}


void reconnect() {
  while (!client.connected()) {
    Serial.print("Tentando conexão MQTT...");
    String clientId = "ESP32Client-" + String(random(0xffff), HEX);
    // if (client.connect(clientId.c_str(), "raitecBraco", "Raitec.braco1")) { ---> para conexão com autenticação, mudar os valores com usuario e senha, respectivamente
    if (client.connect(clientId.c_str())) {
      Serial.println("conectado");
      client.subscribe("ufc/raitec/braco/comando");
    } else {
      Serial.printf("falhou, rc=%d, tentando de novo em 5s\n", client.state());
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}

