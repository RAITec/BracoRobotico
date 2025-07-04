# README: Comunicação MQTT para Braço Robótico

Este documento detalha o funcionamento e o método de uso dos códigos desenvolvidos para a comunicação MQTT no projeto do Braço Robótico.

## Links e Referências

### Sobre MQTT

  * [E-book MQTT Essentials (HiveMQ)](https://www.hivemq.com/downloads/hivemq-ebook-mqtt-essentials.pdf)
  * [Playlist YouTube - MQTT Básico](https://youtu.be/bBfHV2nM_PU%3Fsi%3DpBPUnZp1d1W7jhoJ)

### Documentação e Ferramentas

  * [Documentação da biblioteca Paho MQTT (Python)](https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html)
  * [Página da biblioteca Paho MQTT no PyPI](https://pypi.org/project/paho-mqtt/)
  * [Servidor MQTT (HiveMQ Cloud)](https://www.hivemq.com/)

## Introdução

O projeto do Braço Robótico requer um protocolo de comunicação eficiente e com baixo consumo de recursos. A escolha do MQTT se deu pela sua leveza e adequação a ambientes com conexão Wi-Fi instável, como o Latin, ao mesmo tempo em que permite a comunicação necessária para o controle do braço.

Este projeto implementa a biblioteca Paho MQTT em Python, facilitando a comunicação bidirecional entre um dispositivo de controle (por exemplo, um computador ou outro microcontrolador) e uma ESP32 conectada ao braço robótico.

## Funcionalidades

A comunicação MQTT é gerenciada através de uma classe `ClienteMqtt`, que encapsula os detalhes da biblioteca Paho MQTT. Isso proporciona uma interface simplificada para o usuário, permitindo o uso de métodos pré-definidos com parâmetros claros, sem a necessidade de gerenciar as complexidades internas do protocolo.

A lógica de comunicação do projeto é dividida em três etapas principais:

1.  **Conexão**
2.  **Comunicação (Publicação/Inscrição)**
3.  **Desconexão**

### 1\. Conexão

A etapa de conexão estabelece a ponte entre o cliente (seu código) e o servidor (broker) MQTT. Para isso, são necessários os seguintes parâmetros:

  * **URL do servidor (broker\_url)**: O endereço do servidor MQTT ao qual o cliente tentará se conectar. Ex: `mqtt.example.com` ou um endereço IP.
  * **Username**: Nome de usuário para autenticação no servidor MQTT (se exigido).
  * **Senha**: Senha para autenticação no servidor MQTT (se exigido).
  * **ID do cliente (client\_id)**: Um identificador único para este cliente na rede MQTT. Cada cliente conectado ao broker deve ter um ID único.
  * **Keepalive (opcional)**: Um valor em segundos que define o intervalo máximo de tempo permitido entre as mensagens enviadas por um cliente ou pelo servidor sem que haja comunicação. Se nenhuma mensagem for trocada dentro desse período, o cliente ou o servidor envia uma mensagem de "ping" para manter a conexão ativa e verificar a disponibilidade da outra parte. Também serve como um "timeout" para detectar conexões perdidas.

Com esses dados, uma instância da classe `ClienteMqtt` é criada. Em seguida, os métodos `conectar()` e `loop_start()` são invocados:

  * `conectar()`: Tenta estabelecer a conexão com o broker MQTT usando os dados fornecidos.
  * `loop_start()`: Inicia uma nova thread em segundo plano que gerencia todo o tráfego de rede MQTT (envio e recebimento de mensagens, pings de keepalive, reconexão automática, etc.). Isso permite que o código principal continue sua execução sem ser bloqueado pelas operações de rede do MQTT.

**Exemplo de Uso:**

```python
import mqttClass as cmqtt # Supondo que mqttClass é o módulo da sua classe ClienteMqtt

# Defina suas variáveis de conexão (idealmente em um arquivo de configuração ou variáveis de ambiente)
BROKER_URL = "seu_broker.com"
USERNAME = "seu_usuario"
PASSWORD = "sua_senha"
CLIENT_ID = "braço_robotico_cliente"
KEEPALIVE = 60 # segundos

# Cria uma instância do ClienteMqtt
clienteMQTT = cmqtt.ClienteMqtt(
    broker_url=BROKER_URL,
    username=USERNAME,
    password=PASSWORD,
    client_id=CLIENT_ID,
    keepalive=KEEPALIVE
)

# Tenta conectar e iniciar o loop de comunicação
try:
    clienteMQTT.conectar()
    clienteMQTT.loop_start()
    print("Conexão MQTT estabelecida e loop iniciado.")
except Exception as e:
    print(f"Erro ao conectar ou iniciar o loop MQTT: {e}")

# O código principal pode continuar aqui enquanto a comunicação MQTT ocorre em segundo plano
```

**Observação:** É altamente recomendável envolver as chamadas a `conectar()` e `loop_start()` em blocos `try-except` para lidar com possíveis exceções (erros de conexão, credenciais inválidas, etc.).

### 2\. Comunicação (Publicação e Inscrição)

Após a conexão bem-sucedida, o cliente MQTT pode enviar e receber mensagens através dos métodos `publicar()` e `inscrever()`.

  * `publicar(topico: str, mensagem: str)`: Envia uma `mensagem` (string) para um `topico` específico (string) no broker MQTT. Qualquer cliente inscrito nesse tópico receberá a mensagem.

    **Exemplo:**

    ```python
    clienteMQTT.publicar("braço/comando", "mover_para_frente")
    ```

  * `inscrever(topico: str)`: Faz com que o cliente se inscreva em um `topico` específico (string). A partir desse momento, o cliente passará a receber todas as mensagens publicadas nesse tópico pelo broker. As mensagens recebidas serão tratadas por uma função de callback definida na sua classe `ClienteMqtt` (geralmente `on_message`).

    **Exemplo:**

    ```python
    clienteMQTT.inscrever("braço/status")
    # As mensagens do tópico "braço/status" serão agora recebidas pelo cliente.
    ```

### 3\. Desconexão

Para encerrar a sessão MQTT de forma controlada, os seguintes métodos devem ser utilizados:

  * `desconectar()`: Envia uma mensagem de desconexão ao broker e encerra a conexão.
  * `loop_stop()`: Interrompe a thread de comunicação iniciada por `loop_start()`, liberando os recursos associados.

**Exemplo de Uso:**

```python
# Após a comunicação ser concluída ou quando o programa for encerrado
try:
    clienteMQTT.desconectar()
    clienteMQTT.loop_stop()
    print("Desconexão MQTT realizada com sucesso.")
except Exception as e:
    print(f"Erro ao desconectar ou parar o loop MQTT: {e}")
```

**Observação:** Assim como na conexão, é aconselhável usar blocos `try-except` ao chamar `desconectar()` e `loop_stop()` para gerenciar possíveis erros durante o encerramento.
