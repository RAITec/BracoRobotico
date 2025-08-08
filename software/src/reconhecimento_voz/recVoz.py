#!/usr/bin/env python3
from vosk import Model , KaldiRecognizer
import pyaudio
import json
import os
# from ..transmissao_dados import mqttClass as cmqtt



BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

VOSK_DIR = os.path.join(BASE_DIR, "voskoff")
os.makedirs(VOSK_DIR, exist_ok=True)

MODEL_PATHS = {
1: os.path.join(VOSK_DIR, "modelo_test1") , # Setor de angulos precisos
2: os.path.join(VOSK_DIR, "modelo_test2") , # Setor pra varios servos
3: os.path.join(VOSK_DIR, "modelo_test3") # Setor de comandos rapidos
}


class ReconhecedorVoz:
    """
    Uma classe que permite usar os recursos de recebimento de voz com Vosk e PyAudio.
    """

    def __init__(self, testeId = 2):

        """
        Inicializa o reconhecedor de voz.

        :param testeId: O numero do modelo de teste que irá utilizar para o reconhecedor
        """


        if(testeId < 0 or testeId > 3):
            self.caminho_modelo = MODEL_PATHS[2]

        else:
            self.caminho_modelo = MODEL_PATHS[testeId]

        try:
            self.modelo = Model(self.caminho_modelo)
        except Exception as e:
            print(f"Erro ao carregar o modelo Vosk em '{self.caminho_modelo}'. "
                  f"Verifique o caminho e se a pasta do modelo está completa. Erro: {e}")
            raise

        self.recognizer = KaldiRecognizer(self.modelo, 16000)

        self._p = pyaudio.PyAudio()
        self._stream = self._p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8192
        )

        

    def escutar(self, on_comando_reconhecido, tratam_dados):
        """
        Inicia a escuta contínua e processa os comandos de voz.
        O cleanup do stream é feito fora do loop principal para evitar fechamento prematuro.
        """
        print("Ouvindo... (Pressione Ctrl+C para encerrar)")
        self._stream.start_stream()

        try:
            while True:
                data = self._stream.read(4096, exception_on_overflow=False)
                if self.recognizer.AcceptWaveform(data):
                    resultado = json.loads(self.recognizer.Result())
                    texto = resultado.get("text", "").strip()

                    texto_limpo = (
                        texto.replace("!SIL", "")
                             .replace("<unk>", "")
                             .strip()
                    )
                    
                    if not texto_limpo:
                        # Ignora silêncio ou reconhecimento incerto
                        continue

                    print(f"Texto reconhecido: {texto_limpo}")
                    comando_processado = tratam_dados(texto_limpo)

                    # A função de callback só é chamada se houver um comando válido
                    if comando_processado:
                        on_comando_reconhecido(comando_processado)

        except KeyboardInterrupt:
            print("\nEncerrando a escuta por solicitação do usuário.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado durante a escuta: {e}")
        finally:
            # Este bloco agora só executa quando o loop é quebrado
            print("\nEncerrando sistema de áudio...")
            if self._stream and self._stream.is_active():
                self._stream.stop_stream()
            if self._stream and not self._stream.is_stopped():
                self._stream.close()
            self._p.terminate()
            print("Recursos de áudio liberados.")

if(__name__ == '__main__'):
        rec = ReconhecedorVoz(testeId=2)
        print("Oioioioioioiio")



        




