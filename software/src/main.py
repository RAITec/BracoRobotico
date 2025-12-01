#!/usr/bin/env python3
from transmissao_dados import mqttClass as cmqtt
from reconhecimento_voz import recVoz
from tratamento_dados.tratamentoDados import (
    processar_teste1,
    processar_teste2,
    processar_teste3
)

processar_testes = {
    1: processar_teste1,
    2: processar_teste2,
    3: processar_teste3
}

TESTE_ATIVO = 2
# Verificar se o tópico utilizado bate com o tópico em que a ESP32 está se inscrevendo.
# Caso não esteja, modifique preferencialmente aqui
MQTT_TOPIC = f"mqtt/teste{TESTE_ATIVO}"

def comando_servo(payload: str):
    """
    Função intermediária para a função escutar, evitando TypeError.

    :param payload: String a ser enviada
    """
    clienteMQTT.publicar(MQTT_TOPIC, payload)

BROKER_URL = "5b7bc54bc63a4ffd9ddc2fa23cf8fa44.s1.eu.hivemq.cloud" # Não mais ativo
USERNAME = "filipeaufc" # Servidor online não mais ativo. É necessário criar um próprio
PASSWORD = "Tdmndmslgr1" # Existem diversas opções para servidor online gratuitas. HiveMQ é a opção que utilizamos
CLIENT_ID = "filipeeac_classe" # Cliente arbitrário
KEEPALIVE = 60
PORT = 8883 # Apesar que o valor default para port já é 8883, a definição explícita padroniza o uso

clienteMQTT = cmqtt.ClienteMqtt(
        broker_url=BROKER_URL,
        username=USERNAME,
        password=PASSWORD,
        client_id=CLIENT_ID,
        keepalive=KEEPALIVE
        port=PORT
    )

try:
    clienteMQTT.conectar()
    clienteMQTT.loop_start()
    tratar_comando = processar_testes[TESTE_ATIVO]
    recc = recVoz.ReconhecedorVoz(testeId=TESTE_ATIVO)
    recc.escutar(on_comando_reconhecido=comando_servo, tratam_dados=tratar_comando)

except Exception as e:
    print(f"Erro: {e}")
except KeyError:
    raise ValueError(f"Opção {TESTE_ATIVO} inválida")

finally:
    clienteMQTT.desconectar()
    clienteMQTT.loop_stop()
