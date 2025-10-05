# app.py

# --- INÍCIO DA MODIFICAÇÃO ---
import sys
import os

# 1. Descobre o caminho absoluto para a pasta 'src'
# os.path.dirname(__file__) -> pega o caminho da pasta atual (app/)
# os.path.abspath(...) -> garante que o caminho seja absoluto
# ... .join(..., '..') -> sobe um nível
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# 2. Adiciona a pasta 'src' à lista de busca de módulos do Python
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)



import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window


from transmissao_dados.mqttClass import ClienteMqtt
from reconhecimento_voz.recVoz import ReconhecedorVoz
from tratamento_dados.tratamentoDados import processar_teste2

# --- 2. Definindo a Aparência (Widget Raiz) ---
# Esta classe vazia se conecta ao design no arquivo .kv
class RootWidget(BoxLayout):
    pass

# --- 3. A Classe Principal do Aplicativo (O Maestro) ---
class AppBracoRobotico(App):
    
    def build(self):
        """
        Constrói a interface a partir do arquivo .kv e inicializa as variáveis de estado.
        """
        Window.clearcolor = (0.05, 0.05, 0.1, 1) # Define a cor de fundo da janela
        self.cliente_mqtt = None
        self.reconhecedor = None
        self.comando_recebido_evento = threading.Event()
        return RootWidget()

    def on_start(self):
        """
        Chamado após a janela ser criada. Inicia as conexões e os serviços de hardware.
        """
        self.root.ids.rotulo_status.text = "Iniciando sistemas..."
        
        # Inicia a conexão MQTT em uma thread para não travar o app se a rede estiver lenta
        threading.Thread(target=self.conectar_servicos).start()

    def conectar_servicos(self):
        """
        Conecta ao Broker MQTT e inicializa o reconhecedor de voz.
        Roda em uma thread separada para manter a UI responsiva.
        """
        # --- Conexão MQTT ---
        try:
            self.agendar_atualizacao_ui("Conectando ao Broker MQTT...")
            self.cliente_mqtt = ClienteMqtt(
                broker_url="5b7bc54bc63a4ffd9ddc2fa23cf8fa44.s1.eu.hivemq.cloud",
                username="filipeaufc",
                password="Tdmndmslgr1",
                client_id="app_kivy_braco_robotico_v2", # ID de cliente único
                port=8883
            )
            self.cliente_mqtt.conectar()
            self.cliente_mqtt.loop_start()
            self.agendar_atualizacao_ui("Conectado ao Broker MQTT.")
        except Exception as e:
            self.agendar_atualizacao_ui(f"Erro no MQTT: {e}")
            return

        # --- Inicialização do Reconhecedor de Voz ---
        try:
            self.agendar_atualizacao_ui("Iniciando sistema de áudio...")
            self.reconhecedor = ReconhecedorVoz(testeId=2)
            self.agendar_atualizacao_ui("Pronto para ouvir. Pressione o botão.")
        except Exception as e:
            self.agendar_atualizacao_ui(f"Erro no Vosk/Áudio: {e}")

    def iniciar_fluxo_de_voz(self):
        """
        Dispara a thread que irá ouvir, processar e enviar o comando.
        """
        self.root.ids.botao_falar.disabled = True
        self.root.ids.rotulo_status.text = "Ouvindo..."
        # Limpa o evento anterior antes de iniciar um novo ciclo
        self.comando_recebido_evento.clear()
        threading.Thread(target=self.thread_ouvir_e_enviar).start()

    def thread_ouvir_e_enviar(self):
        """
        Função que roda em segundo plano.
        Ela inicia a escuta e fica esperando o sinal para terminar.
        """
        if not self.reconhecedor:
            self.agendar_atualizacao_ui("Erro: Reconhecedor não iniciado.")
            return

        try:
            # Inicia a escuta em uma nova thread para não bloquear esta
            escuta_thread = threading.Thread(
                target=self.reconhecedor.escutar,
                args=(self.callback_receber_e_parar, processar_teste2)
            )
            escuta_thread.daemon = True  # Permite que o app feche mesmo se a thread estiver presa
            escuta_thread.start()

            # Espera pelo sinal (com um timeout para não travar para sempre)
            # O método 'escutar' nunca termina, então precisamos de um jeito de parar
            # A função de callback vai nos dar esse sinal
            sinal_recebido = self.comando_recebido_evento.wait(timeout=20.0) # Espera 20 segundos

            if not sinal_recebido:
                self.agendar_atualizacao_ui("Tempo esgotado. Nenhum comando detectado.")
                # Como não podemos parar a thread 'escutar' diretamente,
                # a melhor abordagem é apenas seguir em frente e deixar a UI usável.

        except Exception as e:
            self.agendar_atualizacao_ui(f"Erro na thread de escuta: {e}")

    def callback_receber_e_parar(self, comando):
        """
        Esta função é passada para o `reconhecedor.escutar`.
        Ela é chamada de dentro do loop do `recVoz.py` quando um comando é reconhecido.
        """
        if self.comando_recebido_evento.is_set():
            # Se já recebemos um comando neste ciclo, ignoramos os seguintes
            return

        # 1. Atualiza a UI e envia o comando
        self.agendar_atualizacao_ui(f"Comando: {comando}. Enviando...")
        self.cliente_mqtt.publicar("braco/comando", comando)
        self.agendar_atualizacao_ui(f"Comando '{comando}' enviado!")

        # 2. "Levanta a bandeira" para sinalizar que terminamos
        self.comando_recebido_evento.set()

    def agendar_atualizacao_ui(self, mensagem):
        Clock.schedule_once(lambda dt: self.atualizar_ui(mensagem))

    def atualizar_ui(self, mensagem):
        self.root.ids.rotulo_status.text = mensagem
        self.root.ids.botao_falar.disabled = False

    def on_stop(self):
        print("Encerrando conexões...")
        if self.cliente_mqtt:
            self.cliente_mqtt.desconectar()
            self.cliente_mqtt.loop_stop()

# --- Ponto de Entrada Principal ---
if __name__ == '__main__':
    AppBracoRobotico().run()