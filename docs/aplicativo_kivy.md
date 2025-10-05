# Guia do Aplicativo - Braço Robótico

---

## 1. Objetivos e necessidades

O objetivo deste documento é implementar o Módulo de Interface Gráfica com a funcionalidade de uma aplicação que facilite as testagens e implementações do software do projeto do braço robótico, desenvolvido no ano de 2025, por meio da **Kivy**, uma biblioteca Python de código aberto usada para criar interfaces gráficas (GUIs) para aplicativos desktop e móveis que rodam em diversas plataformas, como Windows, macOS, Linux, Android e iOS. A necessidade de se criar esse app, surgiu para diminuir a poluição visual causada ao acessar IDEs como o VScode para rodar o código de reconhecimento de voz e da comunicação, bem como ter uma interface mais acessível para quem for usar o braço robótico.

Para mais informações sobre as funcionalidades da Kivy bem como guias de programação e exemplos, acesse o site oficial clicando [aqui](https://kivy.org/doc/stable/).

## 2. Arquitetura do sistema

- **Módulo de Interface Gráfica (app.py no repositório):** O ponto de entrada para o usuário. Apresenta os botões e o status do sistema.
- **Módulo de Reconhecimento de Voz (recVoz.py no repositório):** Este script é responsável por usar a biblioteca Vosk e PyAudio para acessar o microfone do seu computador, ouvir o que você diz e transformar o áudio em texto.
- **Módulo de Tratamento de dados (tratamentoDados.py no repositório):** Este é o "tradutor". Ele pega o texto bruto gerado pelo recVoz.py (ex: "servo um noventa") e, usando dicionários, o converte em um comando padronizado que o robô entende (ex: "SERVO1:90").
- **Módulo de Transmissão de dados (mqttClass.py):** Este script usa a biblioteca paho-mqtt para se conectar a um "servidor de mensagens" (chamado Broker MQTT) e enviar os comandos para a ESP32.
- **Módulo de movimentação (ESP32, Servos e ArduinoIDE):** O microcontrolador recebe o comando via MQTT e aciona os servomotores correspondentes por meio de uma lógica feita no Arduíno IDE.

**Observação 1:** Os guias do reconhecimento, processamento, comunicação e lógica de movimentação se encontram em outros guias ou no GitHub do projeto.

## 3. Requisitos e configuração do ambiente

Antes de iniciar a criação e em si do aplicativo, iremos presumir que você já tenha acesso aos códigos e instalações específicas dos outros módulos, caso não, pode encontrá-los aqui:

[O repositório do braço robótico](https://github.com/RAITA-UFC/BracoRobotico).

Entretanto podemos fazer um resumo rápido do que se precisa para o nosso app funcionar já que o foco aqui não é instalar as ferramentas dos outros módulos.

**Observação:** sempre use um ambiente virtual (venv) para instalar as dependências com o objetivo de não causar conflito de versões e bibliotecas do seu computador.

Abra o terminal e faça:

### no Windows:

```bash
# Verificar se Python esta instalado
python --version
# ou
py --version

# Criar ambiente virtual
py -m venv .venv
# ou
python -m venv .venv

# Ativar o ambiente virtual
.venv\Scripts\activate

# Verificar se esta funcionando
python --version
```

### no Linux:

```bash
# Verificar Python
python3 --version

# Criar venv
python3 -m venv .venv

# Ativar venv
source .venv/bin/activate

# 4. Verificar que esta usando a venv
which python
python --version
```

Tendo feito isso aparecerá um (venv) no seu terminal.

Para a instalação das bibliotecas em python necessárias você obrigatoriamente irá precisar do pip, o gerenciador de pacotes python.

Por fim, tanto no linux quanto no windows você pode instalar as bibliotecas dessa maneira:

```bash
pip install vosk
pip install paho-mqtt
pip install kivy
```

Sendo o vosk para reconhecimento de voz, o paho-mqtt para a transmissão de dados e o kivy para o aplicativo.

## 4. Estrutura Básica de um App Kivy

Todo aplicativo Kivy é construído em torno de uma classe que herda de ‘App‘. O ponto de entrada é o método ‘build‘, que retorna o widget raiz da interface. O aplicativo é iniciado chamando o método ‘run‘.

```python
from kivy.app import App # Importa a classe base para criar o aplicativo
from kivy.uix.label import Label # Importa o widget Label, usado para exibir texto

class MeuPrimeiroApp(App): # A classe do app deve sempre herdar de ‘App‘ e terminar com "App"
    def build(self):
        """
        Este eh o metodo central do aplicativo Kivy.
        Ele eh obrigatorio e deve retornar um widget (a raiz da arvore de interface).
        E aqui que toda a UI principal e construida.
        """
        return Label(text='Ola, RAITec! Este e meu primeiro app Kivy.') # Cria e retorna um widget Label com o texto especificado

if __name__ == '__main__':
    """
    Este bloco define o ponto de entrada do programa.
    So sera executado se o script for rodado diretamente (e nao importado como modulo).
    """
    app = MeuPrimeiroApp() # Cria uma instancia da nossa classe de aplicativo
    app.run() # Inicia o ciclo de vida do aplicativo Kivy: cria a janela, inicia o loop de eventos e desenha a UI
```

### 4.1 Fluxo de Vida do Aplicativo Kivy

O ciclo de vida de um app Kivy, gerenciado pela classe ‘App‘, segue esta sequência:

1.  **Inicialização:** O aplicativo é instanciado e o método ‘build‘ é chamado.
2.  **Execução:** O método ‘run‘ inicia o loop de eventos da aplicação.
3.  **Eventos:** O app responde a entradas do usuário (toques, cliques, teclado) e redimensionamentos de tela.
4.  **Encerramento:** Quando a janela é fechada, o app finaliza sua execução.

### 4.2 Métodos Úteis da Classe ‘App‘

Além do ‘build‘, a classe ‘App‘ possui outros métodos que você pode sobrescrever para customizar o comportamento:

```python
class MeuApp(App):
    def on_start(self):
        """Chamado quando o aplicativo esta inicializando, antes do ‘build‘."""
        pass

    def on_stop(self):
        """Chamado quando o aplicativo esta terminando sua execucao."""
        pass

    def on_pause(self):
        """
        Chamado quando o aplicativo e pausado (importante em dispositivos moveis).
        Se retornar True, o app pode ser retomado posteriormente.
        """
        return True

    def on_resume(self):
        """Chamado quando o aplicativo e retomado apos uma pausa."""
        pass
```

## 5. Construção do Aplicativo: Lógica e Design

Para criar nossa interface gráfica, a arquitetura do Kivy nos incentiva a separar a lógica da aplicação (o que os botões fazem, como os dados são processados) da sua apresentação visual (cores, tamanhos, layout). Para isso, trabalharemos com dois arquivos principais: um arquivo Python (app.py) para a lógica e um arquivo de linguagem Kivy (appbracorobotico.kv) para o design, você pode encontrar os dois no repositório do GitHub.

### 5.1 O Design da Interface (appbracorobotico.kv)

Primeiro, definimos a aparência do nosso aplicativo. O arquivo com formato .kv é o responsável por organizar o design, o layout e as cores dos elementos visuais. Ele descreve a hierarquia dos widgets (botões, rótulos) e conecta as ações do usuário, como um clique de botão (on_press), a funções que serão definidas no nosso arquivo Python. Este arquivo é puramente declarativo, focando em ”o que”aparece na tela e ”como”se parece, sem se preocupar com a lógica de execução.

### 5.2 A Lógica da Aplicação (app.py)

Esse código é o cerne do aplicativo, ele vai atuar como o "maestro"que importa e orquestra nossos módulos já existentes de reconhecimento de voz, processamento e comunicação. Mas ainda temos um outro detalhe, esse código não apenas importa as ferramentas, mas também apresenta a lógica de como vai funcionar nosso app e o que cada botão faz (os eventos).

Ele é responsável por:

-   Inicializar e gerenciar as conexões (MQTT) e os serviços de hardware (microfone via Vosk).
-   Definir as funções que são chamadas quando os botões definidos no arquivo .kv são pressionados.
-   Orquestrar o fluxo de dados: chamar o reconhecimento de voz, passar o resultado para o processamento e enviar o comando final via MQTT.
-   Atualizar a interface do usuário com mensagens de status, como ”Ouvindo...”ou ”Comando enviado!”.

Em resumo, o arquivo .kv define a aparência estática e os ”gatilhos”de eventos, enquanto o arquivo app.py contém a lógica dinâmica que dá vida ao aplicativo, respondendo a esses gatilhos e gerenciando os processos em segundo plano.

Ao executar finalmente o app.py obtemos algo como:

*O que deve aparecer na sua tela.*

## 6. Guia de Uso Rápido

Este guia descreve os passos para executar o aplicativo a partir do código-fonte, considerando a estrutura de pacotes do projeto.

1.  **Abra o Terminal:** Inicie um terminal (Prompt de Comando, PowerShell ou Terminal do VS Code) e navegue até a pasta raiz do projeto, chamada `BracoRobotico/`.
2.  **Ative o Ambiente Virtual:** Execute o seguinte comando para ativar o ambiente virtual onde todas as dependências estão instaladas.

    **Windows:**

    ```
    .\venv\Scripts\activate
    ```

    **Linux:**

    ```
    source .venv/bin/activate
    ```

    **Observação:** O seu prompt de comando deverá agora exibir o prefixo `(venv)`.

3.  **Execute o Aplicativo:** Digite o comando abaixo para iniciar a aplicação. Este comando executa o script principal localizado dentro da estrutura de pacotes do software.

    ```
    python software/src/app/app.py
    ```

4.  **Aguarde a Inicialização:** A janela do aplicativo aparecerá. Observe o campo de status no topo. Ele deve exibir a mensagem "Pronto para ouvir. Pressione o botão.".

    -   Se uma mensagem de erro do MQTT aparecer (ex: ”No route to host”ou ”Connection refused”), verifique se o seu computador está conectado à internet e se a ESP32 está ligada e online.

5.  **Pressione para Falar:** Clique e mantenha pressionado o bot˜ao principal que diz "Pressione para Falar". O status mudará para "Ouvindo...".
6.  **Fale um Comando Válido:** Enquanto segura o botão, fale um comando claro, como por exemplo: ”servo um noventa graus” ou ”garra abrir”
7.  **Observe o Resultado:** Solte o botão. O campo de status será atualizado, mostrando o texto que foi reconhecido e, em seguida, a confirmação de que o comando foi enviado. O botão ficará habilitado novamente para um novo comando.

## 7. Limitações e possíveis implementações futuras

-   Melhorar a arte dos botões, já que o aplicativo possui um design default e não personalizado.
-   Lógica para mudar o IP diretamente no aplicativo e não no código, já que se mudamos de rede temos que colocar um novo IP no código da main.py e do reconhecimento
-   Tornar o aplicativo empacotado disponível para outras pessoas, sem a necessidade de baixar todas as dependências como vosk, paho-MQTT e etc, já que toda vez que queremos usar o aplicativos teremos que baixar todas essas coisas para ele funcionar, otimizar isso seria um ótimo passo e avanço nesse projeto.

