# Documentação: Configuração do Mosquitto Broker

Este documento detalha os passos para instalar e configurar um broker Mosquitto em um sistema Ubuntu, com foco em criar uma configuração local segura com autenticação por usuário e senha.

## Links e Referências

* **Documentação Oficial**
    * [Site Oficial do Mosquitto](https://mosquitto.org/): A fonte primária de documentação do broker.
    * [Site Oficial do Protocolo MQTT](https://mqtt.org/): Para entender as especificações do padrão.

* **Aprendizado e Tutoriais**
    * [E-book MQTT Essentials (HiveMQ)](https://www.hivemq.com/downloads/hivemq-ebook-mqtt-essentials.pdf): Um livro completo sobre os fundamentos do protocolo MQTT.
    * [DigitalOcean Mosquitto Tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-the-mosquitto-mqtt-messaging-broker-on-ubuntu-18-04): Um guia prático e completo de instalação e segurança.

* **Ferramentas de Depuração (Clientes GUI)**
    * [MQTT Explorer](http://mqtt-explorer.com/): Cliente desktop para visualizar tópicos e mensagens em tempo real. Essencial para desenvolvimento.
-----

## 1\. Instalação via PPA

Existem algumas formas de instalar o Mosquitto, mas para garantir a versão mais recente, usaremos o repositório PPA oficial.

#### Passos da Instalação

Execute os seguintes comandos em sequência para adicionar o PPA, atualizar a lista de pacotes e instalar o broker e os clientes de linha de comando.

```bash
sudo apt update
sudo add-apt-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt update
sudo apt-get install mosquitto mosquitto-clients
```

-----

## 2\. Verificação Pós-Instalação

Após a instalação, é importante verificar se tudo ocorreu bem.

#### 2.1. Verificando o Binário

Use o comando `which` para confirmar que o executável do Mosquitto está no PATH do sistema.

```bash
which mosquitto
```

A saída deve ser algo como: `/usr/sbin/mosquitto`

#### 2.2. Verificando o Status do Serviço

Verifique se o serviço do Mosquitto está ativo e rodando com `systemctl`.

```bash
sudo systemctl status mosquitto
```

A saída deve indicar `Active: active (running)`:

```
● mosquitto.service - Mosquitto MQTT Broker
     Loaded: loaded (/lib/systemd/system/mosquitto.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2025-09-28 19:25:10 -03; 15s ago
...
```

> Pressione `q` para sair da visualização de status. Caso o serviço esteja inativo, inicie-o com: `sudo systemctl start mosquitto`

-----

## 3\. Teste Inicial (Conexão Anônima)

Por padrão, a instalação permite conexões anônimas. Vamos confirmar que o broker está funcional.

1.  **Abra um terminal (Terminal 1)** e inicie um "subscriber" para escutar mensagens no tópico `teste/topico`.

    ```bash
    mosquitto_sub -h localhost -t "teste/topico"
    ```

2.  **Abra outro terminal (Terminal 2)** e use um "publisher" para enviar uma mensagem ao mesmo tópico.

    ```bash
    mosquitto_pub -h localhost -t "teste/topico" -m "Ola, Mosquitto!"
    ```

No **Terminal 1**, a mensagem "Ola, Mosquitto\!" deve aparecer instantaneamente. Isso confirma que o broker está funcionando, mas de forma insegura.

-----

## 4\. Configuração de Segurança

Agora, vamos desabilitar o acesso anônimo e forçar o uso de usuário e senha para garantir um mínimo de segurança.

#### 4.1. Criação do Arquivo de Senhas

Usaremos a ferramenta `mosquitto_passwd` para criar um arquivo que armazenará os usuários e senhas.

O comando abaixo usa a flag `-c` para **criar** o arquivo e adicionar o primeiro usuário. Substitua `seu_usuario` pelo nome desejado.

```bash
sudo mosquitto_passwd -c /etc/mosquitto/passwd seu_usuario
```

Você será solicitado a digitar e confirmar a senha para este usuário.

#### 4.2. Ajuste de Permissões do Arquivo

Por segurança, o arquivo de senhas não deve ser legível por qualquer usuário. Precisamos restringir o acesso apenas ao serviço do Mosquitto.

```bash
# Muda o proprietário do arquivo para o usuário 'mosquitto'
sudo chown mosquitto:mosquitto /etc/mosquitto/passwd

# Garante que apenas o proprietário possa ler o arquivo
sudo chmod 600 /etc/mosquitto/passwd
```

#### 4.3. Criação do Arquivo de Configuração Local

Vamos criar um arquivo de configuração personalizado no diretório `conf.d`.

```bash
sudo nano /etc/mosquitto/conf.d/minha_conf.conf
```

Dentro do editor, cole o seguinte conteúdo:

```conf
# =================================================================
# Configuração simples para o projeto Braço Robótico
# Esta configuração funciona para Mosquitto 2.0.18
# Obs: e versões anteriores (eu acho)
# =================================================================

# -----------------------------------------------------------------
# Configurações Globais
# -----------------------------------------------------------------
persistence false
allow_anonymous false
password_file /etc/mosquitto/passwd
log_dest file /var/log/mosquitto/mosquitto.log

# -----------------------------------------------------------------
# Bloco do Listener 1: Conexão Insegura
# Este listener permite conexão de até 20 usuários simultâneos
# Obs: ver documentação para mais opções personalizadas para listener
# -----------------------------------------------------------------
listener 1883 0.0.0.0
socket_domain ipv4
max_connections 20

# -----------------------------------------------------------------
# Bloco do Listener 2: Conexão Segura com TLS - não necessário para o Braço
# Precisa de passos adicionais para implementar. Se quiser,
# olhar documentação do mosquitto sobre configuração TLS
# (As opções de TLS se aplicam ao listener 8883)
# -----------------------------------------------------------------
# listener 8883 0.0.0.0
# socket_domain ipv4
# max_connections 20
# cafile /etc/mosquitto/ca_certificates/ca.crt
# certfile /etc/mosquitto/certs/server.crt
# keyfile /etc/mosquitto/certs/server.key
# tls_version tlsv1.2
```

-----

## 5\. Aplicando a Configuração e Teste Final

#### 5.1. Reiniciar o Serviço

Para que a nova configuração seja carregada, reinicie o serviço do Mosquitto.

```bash
sudo systemctl restart mosquitto
```

#### 5.2. Teste Final (Conexão Autenticada)

Agora, a conexão anônima deve falhar e apenas a conexão com usuário e senha deve funcionar.

1.  **Teste de Falha:** Tente se conectar anonimamente.

    ```bash
    mosquitto_sub -h localhost -t "teste/topico"
    ```

    Você deve receber um erro: `Connection Refused: not authorised.` **Isso é o esperado\!**

2.  **Teste de Sucesso:**

      * **No Terminal 1 (Subscriber):** Use suas credenciais para se inscrever. (Substitua `seu_usuario` e `sua_senha`.)
        ```bash
        mosquitto_sub -h localhost -t "teste/topico" -u "seu_usuario" -P "sua_senha"
        ```
      * **No Terminal 2 (Publisher):** Use as mesmas credenciais para publicar.
        ```bash
        mosquitto_pub -h localhost -t "teste/topico" -m "Mensagem segura!" -u "seu_usuario" -P "sua_senha"
        ```

A "Mensagem segura\!" deve aparecer no Terminal 1, confirmando que sua configuração está correta e segura.
