# app.py (Versão com recriação do Reconhecedor para evitar erro do Vosk)

import sys
import os

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
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

class RootWidget(BoxLayout):
    pass

class AppBracoRobotico(App):
    
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.1, 1)
        self.cliente_mqtt = None
        # --- MUDANÇA 1: O Reconhecedor não é mais criado no início ---
        self.reconhecedor = None 
        self.comando_recebido_evento = threading.Event()
        return RootWidget()

    def on_start(self):
        self.root.ids.rotulo_status.text = "Iniciando sistemas..."
        threading.Thread(target=self.conectar_servicos).start()

    def conectar_servicos(self):
        # --- MUDANÇA 2: A conexão de serviços agora só cuida do MQTT ---
        try:
            self.agendar_atualizacao_ui("Conectando ao Broker MQTT...")
            self.cliente_mqtt = ClienteMqtt(
                broker_url="10.13.139.230",
                username="natan",
                password="123456",
                client_id="bracoclient",
                keepalive=180,
                port=1883
            )
            self.cliente_mqtt.conectar()
            self.cliente_mqtt.loop_start()
            self.agendar_atualizacao_ui("Conectado. Pressione o botão para falar.")
        except Exception as e:
            self.agendar_atualizacao_ui(f"Erro no MQTT: {e}")
            return

    def iniciar_fluxo_de_voz(self):
        self.root.ids.botao_falar.disabled = True
        self.root.ids.rotulo_status.text = "Ouvindo..."
        self.comando_recebido_evento.clear()
        threading.Thread(target=self.thread_ouvir_e_enviar).start()

    def thread_ouvir_e_enviar(self):
        """
        Função que roda em segundo plano.
        AGORA ELA CRIA E DESTROI O RECONHECEDOR A CADA CHAMADA.
        """
        # --- MUDANÇA 3: Cria um novo objeto ReconhecedorVoz ---
        try:
            self.reconhecedor = ReconhecedorVoz(testeId=2)
        except Exception as e:
            self.agendar_atualizacao_ui(f"Erro ao iniciar áudio: {e}")
            return

        try:
            escuta_thread = threading.Thread(
                target=self.reconhecedor.escutar,
                args=(self.callback_receber_e_parar, processar_teste2)
            )
            escuta_thread.daemon = True
            escuta_thread.start()

            sinal_recebido = self.comando_recebido_evento.wait(timeout=20.0)

            if not sinal_recebido:
                self.agendar_atualizacao_ui("Tempo esgotado. Nenhum comando detectado.")

        except Exception as e:
            self.agendar_atualizacao_ui(f"Erro na thread de escuta: {e}")
        finally:
            # --- MUDANÇA 4: Garante a destruição do objeto ---
            # Ao setar para None, o Garbage Collector do Python irá chamar o __del__
            # da classe ReconhecedorVoz (se você tiver um), limpando os recursos do PyAudio.
            if self.reconhecedor:
                del self.reconhecedor
                self.reconhecedor = None


    def callback_receber_e_parar(self, comando):
        if self.comando_recebido_evento.is_set():
            return

        self.agendar_atualizacao_ui(f"Comando: {comando}. Enviando...")
        self.cliente_mqtt.publicar("braco/comando", comando)
        self.agendar_atualizacao_ui(f"Comando '{comando}' enviado!")
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

if __name__ == '__main__':
    AppBracoRobotico().run()# app.py (Versão com recriação do Reconhecedor para evitar erro do Vosk)

import sys
import os

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
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

class RootWidget(BoxLayout):
    pass

class AppBracoRobotico(App):
    
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.1, 1)
        self.cliente_mqtt = None
        # --- MUDANÇA 1: O Reconhecedor não é mais criado no início ---
        self.reconhecedor = None 
        self.comando_recebido_evento = threading.Event()
        return RootWidget()

    def on_start(self):
        self.root.ids.rotulo_status.text = "Iniciando sistemas..."
        threading.Thread(target=self.conectar_servicos).start()

    def conectar_servicos(self):
        # --- MUDANÇA 2: A conexão de serviços agora só cuida do MQTT ---
        try:
            self.agendar_atualizacao_ui("Conectando ao Broker MQTT...")
            self.cliente_mqtt = ClienteMqtt(
                broker_url="10.13.139.230",
                username="natan",
                password="123456",
                client_id="bracoclient",
                keepalive=180,
                port=1883
            )
            self.cliente_mqtt.conectar()
            self.cliente_mqtt.loop_start()
            self.agendar_atualizacao_ui("Conectado. Pressione o botão para falar.")
        except Exception as e:
            self.agendar_atualizacao_ui(f"Erro no MQTT: {e}")
            return

    def iniciar_fluxo_de_voz(self):
        self.root.ids.botao_falar.disabled = True
        self.root.ids.rotulo_status.text = "Ouvindo..."
        self.comando_recebido_evento.clear()
        threading.Thread(target=self.thread_ouvir_e_enviar).start()

    def thread_ouvir_e_enviar(self):
        """
        Função que roda em segundo plano.
        AGORA ELA CRIA E DESTROI O RECONHECEDOR A CADA CHAMADA.
        """
        # --- MUDANÇA 3: Cria um novo objeto ReconhecedorVoz ---
        try:
            self.reconhecedor = ReconhecedorVoz(testeId=2)
        except Exception as e:
            self.agendar_atualizacao_ui(f"Erro ao iniciar áudio: {e}")
            return

        try:
            escuta_thread = threading.Thread(
                target=self.reconhecedor.escutar,
                args=(self.callback_receber_e_parar, processar_teste2)
            )
            escuta_thread.daemon = True
            escuta_thread.start()

            sinal_recebido = self.comando_recebido_evento.wait(timeout=20.0)

            if not sinal_recebido:
                self.agendar_atualizacao_ui("Tempo esgotado. Nenhum comando detectado.")

        except Exception as e:
            self.agendar_atualizacao_ui(f"Erro na thread de escuta: {e}")
        finally:
            # --- MUDANÇA 4: Garante a destruição do objeto ---
            # Ao setar para None, o Garbage Collector do Python irá chamar o __del__
            # da classe ReconhecedorVoz (se você tiver um), limpando os recursos do PyAudio.
            if self.reconhecedor:
                del self.reconhecedor
                self.reconhecedor = None


    def callback_receber_e_parar(self, comando):
        if self.comando_recebido_evento.is_set():
            return

        self.agendar_atualizacao_ui(f"Comando: {comando}. Enviando...")
        self.cliente_mqtt.publicar("braco/comando", comando)
        self.agendar_atualizacao_ui(f"Comando '{comando}' enviado!")
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

if __name__ == '__main__':
    AppBracoRobotico().run()# app.py (Versão com recriação do Reconhecedor para evitar erro do Vosk)

import sys
import os

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
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

class RootWidget(BoxLayout):
    pass

class AppBracoRobotico(App):
    
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.1, 1)
        self.cliente_mqtt = None
        # --- MUDANÇA 1: O Reconhecedor não é mais criado no início ---
        self.reconhecedor = None 
        self.comando_recebido_evento = threading.Event()
        return RootWidget()

    def on_start(self):
        self.root.ids.rotulo_status.text = "Iniciando sistemas..."
        threading.Thread(target=self.conectar_servicos).start()

    def conectar_servicos(self):
        # --- MUDANÇA 2: A conexão de serviços agora só cuida do MQTT ---
        try:
            self.agendar_atualizacao_ui("Conectando ao Broker MQTT...")
            self.cliente_mqtt = ClienteMqtt(
                broker_url="10.13.139.230",
                username="natan",
                password="123456",
                client_id="bracoclient",
                keepalive=180,
                port=1883
            )
            self.cliente_mqtt.conectar()
            self.cliente_mqtt.loop_start()
            self.agendar_atualizacao_ui("Conectado. Pressione o botão para falar.")
        except Exception as e:
            self.agendar_atualizacao_ui(f"Erro no MQTT: {e}")
            return

    def iniciar_fluxo_de_voz(self):
        self.root.ids.botao_falar.disabled = True
        self.root.ids.rotulo_status.text = "Ouvindo..."
        self.comando_recebido_evento.clear()
        threading.Thread(target=self.thread_ouvir_e_enviar).start()

    def thread_ouvir_e_enviar(self):
        """
        Função que roda em segundo plano.
        AGORA ELA CRIA E DESTROI O RECONHECEDOR A CADA CHAMADA.
        """
        # --- MUDANÇA 3: Cria um novo objeto ReconhecedorVoz ---
        try:
            self.reconhecedor = ReconhecedorVoz(testeId=2)
        except Exception as e:
            self.agendar_atualizacao_ui(f"Erro ao iniciar áudio: {e}")
            return

        try:
            escuta_thread = threading.Thread(
                target=self.reconhecedor.escutar,
                args=(self.callback_receber_e_parar, processar_teste2)
            )
            escuta_thread.daemon = True
            escuta_thread.start()

            sinal_recebido = self.comando_recebido_evento.wait(timeout=20.0)

            if not sinal_recebido:
                self.agendar_atualizacao_ui("Tempo esgotado. Nenhum comando detectado.")

        except Exception as e:
            self.agendar_atualizacao_ui(f"Erro na thread de escuta: {e}")
        finally:
            # --- MUDANÇA 4: Garante a destruição do objeto ---
            # Ao setar para None, o Garbage Collector do Python irá chamar o __del__
            # da classe ReconhecedorVoz (se você tiver um), limpando os recursos do PyAudio.
            if self.reconhecedor:
                del self.reconhecedor
                self.reconhecedor = None


    def callback_receber_e_parar(self, comando):
        if self.comando_recebido_evento.is_set():
            return

        self.agendar_atualizacao_ui(f"Comando: {comando}. Enviando...")
        self.cliente_mqtt.publicar("braco/comando", comando)
        self.agendar_atualizacao_ui(f"Comando '{comando}' enviado!")
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

if __name__ == '__main__':
    AppBracoRobotico().run()# app.py (Versão com recriação do Reconhecedor para evitar erro do Vosk)

import sys
import os

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
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

class RootWidget(BoxLayout):
    pass

class AppBracoRobotico(App):
    
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.1, 1)
        self.cliente_mqtt = None
        # --- MUDANÇA 1: O Reconhecedor não é mais criado no início ---
        self.reconhecedor = None 
        self.comando_recebido_evento = threading.Event()
        return RootWidget()

    def on_start(self):
        self.root.ids.rotulo_status.text = "Iniciando sistemas..."
        threading.Thread(target=self.conectar_servicos).start()

    def conectar_servicos(self):
        # --- MUDANÇA 2: A conexão de serviços agora só cuida do MQTT ---
        try:
            self.agendar_atualizacao_ui("Conectando ao Broker MQTT...")
            self.cliente_mqtt = ClienteMqtt(
                broker_url="10.13.139.230",
                username="natan",
                password="123456",
                client_id="bracoclient",
                keepalive=180,
                port=1883
            )
            self.cliente_mqtt.conectar()
            self.cliente_mqtt.loop_start()
            self.agendar_atualizacao_ui("Conectado. Pressione o botão para falar.")
        except Exception as e:
            self.agendar_atualizacao_ui(f"Erro no MQTT: {e}")
            return

    def iniciar_fluxo_de_voz(self):
        self.root.ids.botao_falar.disabled = True
        self.root.ids.rotulo_status.text = "Ouvindo..."
        self.comando_recebido_evento.clear()
        threading.Thread(target=self.thread_ouvir_e_enviar).start()

    def thread_ouvir_e_enviar(self):
        """
        Função que roda em segundo plano.
        AGORA ELA CRIA E DESTROI O RECONHECEDOR A CADA CHAMADA.
        """
        # --- MUDANÇA 3: Cria um novo objeto ReconhecedorVoz ---
        try:
            self.reconhecedor = ReconhecedorVoz(testeId=2)
        except Exception as e:
            self.agendar_atualizacao_ui(f"Erro ao iniciar áudio: {e}")
            return

        try:
            escuta_thread = threading.Thread(
                target=self.reconhecedor.escutar,
                args=(self.callback_receber_e_parar, processar_teste2)
            )
            escuta_thread.daemon = True
            escuta_thread.start()

            sinal_recebido = self.comando_recebido_evento.wait(timeout=20.0)

            if not sinal_recebido:
                self.agendar_atualizacao_ui("Tempo esgotado. Nenhum comando detectado.")

        except Exception as e:
            self.agendar_atualizacao_ui(f"Erro na thread de escuta: {e}")
        finally:
            # --- MUDANÇA 4: Garante a destruição do objeto ---
            # Ao setar para None, o Garbage Collector do Python irá chamar o __del__
            # da classe ReconhecedorVoz (se você tiver um), limpando os recursos do PyAudio.
            if self.reconhecedor:
                del self.reconhecedor
                self.reconhecedor = None


    def callback_receber_e_parar(self, comando):
        if self.comando_recebido_evento.is_set():
            return

        self.agendar_atualizacao_ui(f"Comando: {comando}. Enviando...")
        self.cliente_mqtt.publicar("braco/comando", comando)
        self.agendar_atualizacao_ui(f"Comando '{comando}' enviado!")
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

if __name__ == '__main__':
    AppBracoRobotico().run()# app.py (Versão com recriação do Reconhecedor para evitar erro do Vosk)

import sys
import os

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
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

class RootWidget(BoxLayout):
    pass

class AppBracoRobotico(App):
    
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.1, 1)
        self.cliente_mqtt = None
        # --- MUDANÇA 1: O Reconhecedor não é mais criado no início ---
        self.reconhecedor = None 
        self.comando_recebido_evento = threading.Event()
        return RootWidget()

    def on_start(self):
        self.root.ids.rotulo_status.text = "Iniciando sistemas..."
        threading.Thread(target=self.conectar_servicos).start()

    def conectar_servicos(self):
        # --- MUDANÇA 2: A conexão de serviços agora só cuida do MQTT ---
        try:
            self.agendar_atualizacao_ui("Conectando ao Broker MQTT...")
            self.cliente_mqtt = ClienteMqtt(
                broker_url="10.13.139.230",
                username="natan",
                password="123456",
                client_id="bracoclient",
                keepalive=180,
                port=1883
            )
            self.cliente_mqtt.conectar()
            self.cliente_mqtt.loop_start()
            self.agendar_atualizacao_ui("Conectado. Pressione o botão para falar.")
        except Exception as e:
            self.agendar_atualizacao_ui(f"Erro no MQTT: {e}")
            return

    def iniciar_fluxo_de_voz(self):
        self.root.ids.botao_falar.disabled = True
        self.root.ids.rotulo_status.text = "Ouvindo..."
        self.comando_recebido_evento.clear()
        threading.Thread(target=self.thread_ouvir_e_enviar).start()

    def thread_ouvir_e_enviar(self):
        """
        Função que roda em segundo plano.
        AGORA ELA CRIA E DESTROI O RECONHECEDOR A CADA CHAMADA.
        """
        # --- MUDANÇA 3: Cria um novo objeto ReconhecedorVoz ---
        try:
            self.reconhecedor = ReconhecedorVoz(testeId=2)
        except Exception as e:
            self.agendar_atualizacao_ui(f"Erro ao iniciar áudio: {e}")
            return

        try:
            escuta_thread = threading.Thread(
                target=self.reconhecedor.escutar,
                args=(self.callback_receber_e_parar, processar_teste2)
            )
            escuta_thread.daemon = True
            escuta_thread.start()

            sinal_recebido = self.comando_recebido_evento.wait(timeout=20.0)

            if not sinal_recebido:
                self.agendar_atualizacao_ui("Tempo esgotado. Nenhum comando detectado.")

        except Exception as e:
            self.agendar_atualizacao_ui(f"Erro na thread de escuta: {e}")
        finally:
            # --- MUDANÇA 4: Garante a destruição do objeto ---
            # Ao setar para None, o Garbage Collector do Python irá chamar o __del__
            # da classe ReconhecedorVoz (se você tiver um), limpando os recursos do PyAudio.
            if self.reconhecedor:
                del self.reconhecedor
                self.reconhecedor = None


    def callback_receber_e_parar(self, comando):
        if self.comando_recebido_evento.is_set():
            return

        self.agendar_atualizacao_ui(f"Comando: {comando}. Enviando...")
        self.cliente_mqtt.publicar("braco/comando", comando)
        self.agendar_atualizacao_ui(f"Comando '{comando}' enviado!")
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

if __name__ == '__main__':
    AppBracoRobotico().run()
