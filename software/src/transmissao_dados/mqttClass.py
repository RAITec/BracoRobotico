#!/usr/bin/env python3

import logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    filename= '../../tables/logs.log',
    filemode='w'
)

import paho.mqtt.client as mqtt
import ssl
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes

class ClienteMqtt:
    """
    Uma classe para gerenciar uma conexão SEGURA com um broker MQTT,
    encapsulando a configuração, conexão, publicação e desconexão.
    """
    def __init__(self, broker_url, username, password, client_id, keepalive=60):
        """
        Inicializa o cliente MQTT com as configurações necessárias.
        """
        self.broker_url = broker_url
        self.port = 8883
        self.client_id = client_id
        self.username = username
        self.password = password
        self.keepalive = keepalive
        # self.flag = True

        # Inicializa o cliente Paho MQTT
        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=self.client_id,
            protocol=mqtt.MQTTv5
        )

        # Atribui os callbacks internos
        self._configurar_callbacks()

        # Configura autenticação e TLS
        self.client.username_pw_set(username=self.username, password=self.password)
        self.client.tls_set(tls_version=ssl.PROTOCOL_TLS)

        # Configura a reconexão automática
        self.client.reconnect_delay_set(min_delay=1, max_delay=120)

    def _on_connect(self, client, userdata, flags, reasonCode, properties):
        """Callback interna para conexão bem-sucedida."""
        if reasonCode == mqtt.MQTT_ERR_SUCCESS:
            print(f"[SUCESSO] Conectado ao broker com código de razão: {reasonCode}")
        else:
            print(f"[AVISO] Falha na conexão com o broker. Código: {reasonCode}")

    def _on_disconnect(self, client, userdata, disc_flags, reasonCode, properties):
        """Callback interna para desconexão."""
        print(f"[AVISO] Desconectado do broker. Código: {reasonCode}")

    def _on_publish(self, client, userdata, mid, reason_code, properties):
        """Callback interna para publicação confirmada."""
        logging.info(f"Publicação enviada. Message ID: {mid}")
        print(f"[SUCESSO] Publicação confirmada. Message ID: {mid}")

    def _on_connect_fail(self, client, userdata):
        """Callback para falha ao tentar conectar."""
        logging.error("Falha ao tentar se conectar ao broker.")
        print("Ocorreu um erro.")

    def _on_socket_close(self, client, userdata, socket):
        """Callback para fechamento do socket."""
        logging.error("Socket fechado.")
        print("Ocorreu um erro.")

    def _on_message(self, client, userdata, msg):
        """Callback interno para recebimento de mensagens."""
        print("MSG: ", msg)
        logging.info("Mensagem recebida. Mensagem: ", msg)

    def _configurar_callbacks(self):
        """Define os métodos de callback para o cliente MQTT."""
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publish
        self.client.on_message = self._on_message
        self.client.on_connect_fail = self._on_connect_fail
        self.client.on_socket_close = self._on_socket_close

    def conectar(self):
        """
        Tenta se conectar ao broker MQTT.
        """
        try:
            print(f"Tentando conectar ao broker em {self.broker_url}...")
            self.client.connect(
                host=self.broker_url,
                port=self.port,
                keepalive=self.keepalive
            )
        except Exception as e:
            print(f"[ERRO] Não foi possível conectar ao broker: {e}")
            raise  # Propaga a exceção para que o código principal possa tratá-la

    def desconectar(self):
        """
        Desconecta o cliente do broker MQTT.
        """
        print("Desconectando do broker...")
        self.client.disconnect()

    def loop_start(self):
        """
        Inicia o loop de rede em uma thread separada para processar
        as mensagens MQTT em segundo plano.
        """
        print("Iniciando loop de rede MQTT...")
        self.client.loop_start()

    def loop_stop(self):
        """
        Para o loop de rede.
        """
        print("Parando loop de rede MQTT...")
        self.client.loop_stop()

    def publicar(self, topico, payload, qos=2, reter=False, aguardar_publicacao=False, timeout=None):
        """
        Publica uma mensagem em um tópico MQTT.

        :param topico: O tópico MQTT para o qual publicar.
        :param payload: A mensagem a ser enviada.
        :param qos: O nível de Qualidade de Serviço (0, 1 ou 2).
        :param reter: Se a mensagem deve ser retida pelo broker.
        :param aguardar_publicacao: Se deve bloquear até a confirmação da publicação (para QoS > 0).
        :param timeout: Timeout em segundos para aguardar a publicação.
        """

        publish_properties = Properties(PacketTypes.PUBLISH)
        # Adicionar propriedades aqui, se necessário. Ex:
        # publish_properties.MessageExpiryInterval = 30

        print(f"Publicando no tópico '{topico}': '{payload}'")
        msg_info = self.client.publish(
            topic=topico,
            payload=payload,
            qos=qos,
            retain=reter,
            properties=publish_properties
        )
        
        if aguardar_publicacao and qos > 0:
            try:
                msg_info.wait_for_publish(timeout=timeout)
                print("Publicação bloqueante confirmada.")
            except (ValueError, RuntimeError) as e:
                print(f"[ERRO] Erro ao aguardar publicação: {e}")

    def inscrever(self, topico, qos=2):
        """Se increve a um tópico"""
        try:
            subs = self.client.subscribe(topico, qos)
        except Exception as e:
            print(f"[ERRO FATAL] Uma exceção não tratada ocorreu: {e}")

# --- Bloco Principal de Execução ---
if __name__ == "__main__":
    # Configurações movidas para o bloco principal
    BROKER_URL = "5b7bc54bc63a4ffd9ddc2fa23cf8fa44.s1.eu.hivemq.cloud"
    USERNAME = "filipeaufc"
    PASSWORD = "Tdmndmslgr1"
    CLIENT_ID = "filipeeac_classe" # Cliente arbitrário
    KEEPALIVE = 10

    # 1. Instancia a classe do cliente
    meu_cliente_mqtt = ClienteMqtt(
        broker_url=BROKER_URL,
        username=USERNAME,
        password=PASSWORD,
        client_id=CLIENT_ID,
        keepalive=KEEPALIVE
    )

    try:
        # 2. Conecta ao broker
        meu_cliente_mqtt.conectar()

        # 3. Inicia o loop de rede
        meu_cliente_mqtt.loop_start()

        # 4. Publica uma mensagem inicial
        meu_cliente_mqtt.publicar("mqtt/teste", "Eu estou aqui, usando a classe!")

        # Loop de interação com o usuário
        print("\nDigite mensagens para publicar. Digite 'sair' para encerrar.")
        while True:
            entrada = input("Mensagem: ")
            if entrada.lower() == 'sair':
                break
            # Publica a mensagem do usuário e aguarda a confirmação
            meu_cliente_mqtt.publicar("mqtt/teste", payload=entrada, qos=2, aguardar_publicacao=True, timeout=5)

    except Exception as e:
        print(f"[ERRO FATAL] Uma exceção não tratada ocorreu: {e}")
    finally:
        # 5. Desconecta e para o loop de forma segura
        meu_cliente_mqtt.desconectar()
        meu_cliente_mqtt.loop_stop()
        print("Aplicação encerrada.")