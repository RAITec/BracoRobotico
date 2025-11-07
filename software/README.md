# Setup do Projeto Python

## 1. Pre-requisitos

* [Python 3.8+](https://www.python.org/downloads/)
* `pip` (geralmente já vem com o Python)

## 2. Criação do Ambiente Virtual

Recomendamos fortemente o uso de um ambiente virtual para isolar as dependências do projeto.

No terminal, navegue até a pasta 'software' do projeto e execute o comando abaixo para criar um ambiente virtual (a pasta `venv` será criada):

Para linux
```bash
python3 -m venv venv
```

Para windows
```bash
python -m venv venv
```

## 3. Ativação do Ambiente

No Linux (Bash/Zsh):
```bash
source venv/bin/activate
```

No Windows (CMD ou PowerShell):
```bash
.\venv\Scripts\activate
```

Você deve ver o nome do usuário no terminal mudando

## 4. Instalar as Dependências

```bash
pip install -r requirements.txt
```

## 5. Desativar

Quando terminar de trabalhar no projeto, você pode desativar o ambiente virtual a qualquer momento com o comando:
```bash
deactivate
```
