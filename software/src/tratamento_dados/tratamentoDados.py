#!/usr/bin/env python3


#-----------------Dicionarios-------------------

NUMEROS_MAP = {
    "zero" : 0 , "cinco" : 5 , "dez" : 10 , "quinze" : 15 , "vinte" : 20 ,
    "vinte e cinco" : 25 , "trinta" : 30 , "trinta e cinco" : 35 ,
    "quarenta" : 40 , "quarenta e cinco" : 45 , "cinquenta" : 50 ,
    "cinquenta e cinco" : 55 , "sessenta" : 60 , "sessenta e cinco" : 65 ,
    "setenta" : 70 , "setenta e cinco" : 75 , "oitenta" : 80 ,
    "oitenta e cinco" : 85 , "noventa" : 90 , "noventa e cinco" : 95 ,
    "cem" : 100 , "cento e cinco" : 105 , "cento e dez" : 110 ,
    "cento e quinze" : 115 , "cento e vinte" : 120 , "cento e vinte e cinco" : 125 ,
    "cento e trinta" : 130 , "cento e trinta e cinco" : 135 ,
    "cento e quarenta" : 140 , "cento e quarenta e cinco" : 145 ,
    "cento e cinquenta" : 150 , "cento e cinquenta e cinco" : 155 ,
    "cento e sessenta" : 160 , "cento e sessenta e cinco" : 165 ,
    "cento e setenta" : 170 , "cento e setenta e cinco" : 175 ,
    "cento e oitenta" : 180
}
# traduz a palavra pro numero
SERVO_MAP = {
    "um" : 1 , "dois" : 2 , "três" : 3 , "quatro" : 4 , "cinco" : 5
}
# traduz a palavra pro id do servo
DIRECAO_MAP = {
    "cima" : "UP" , "baixo" : "DOWN" , "direita" : "RIGHT" ,
    "esquerda" : "LEFT" , "frente" : "FORWARD" , "trás" : "BACKWARD"
}

GARRA_MAP = {
    "abrir" : "OPEN" , "fechar" : "CLOSE" , "pegar" : "GRAB" , "largar" : "RELEASE"
}

#--------------------------------------------------------



def _extrair_valor_numerico(texto: str) -> int:
    """
    Encontra a sequencia numerica mais longa no texto
    """
    palavras = texto.split()

    melhor_seq = ""
    melhor_valor = 0

    # procura sequencias de 1 a 5 palavras que valem pros mapas, sendo
    # ex: cento e (alguma coisa) e (alguma coisa) -> 5 palavras
    for comprimento in range (5, 0, -1):
        for i in range(len(palavras) - comprimento + 1):
            sequencia = " ".join(palavras[i:i+comprimento])

            if sequencia in NUMEROS_MAP:
                valor = NUMEROS_MAP[sequencia]
                if comprimento > len(melhor_seq.split()):
                    melhor_seq = sequencia
                    melhor_valor = valor
    return melhor_valor

    
def processar_teste1(texto: str):
    if "<unk>" in texto or not texto.strip():
        return None
                    
    if any(p in texto for p in ["sair", "parar", "encerrar", "finalizar"]):
        return "SAIR"
                    
    valor = _extrair_valor_numerico(texto)

    valor = max(0, min(valor, 180))

    if valor > 0:
        return f"SERVO:{valor}"
        
    return None
    
    
def processar_teste2(texto: str):
    if "<unk>" in texto or not texto.strip():
        return None
                    
    if any(p in texto for p in ["sair", "parar", "encerrar", "finalizar"]):
        return "SAIR"
        
    for palavra, acao in GARRA_MAP.items():
        if palavra in texto:
            return f"GARRA:{acao}"
            
    servo_id = None
    for palavra, num in SERVO_MAP.items():
        if palavra in texto:
            servo_id = num
            break

    valor = _extrair_valor_numerico(texto)
    valor = max(0, min(valor, 180))

    if servo_id is not None and valor > 0:
        return f"SERVO{servo_id}:{valor}"
    elif servo_id is None and any(p in texto for p in NUMEROS_MAP):
        return "ERRO: Servo não especificado"
        
    return None
    
    
def processar_teste3(texto: str):
    if "<unk>" in texto or not texto.strip():
        return None
                    
    if texto in DIRECAO_MAP:
        return f"DIR:{DIRECAO_MAP[texto]}"
    if texto in GARRA_MAP:
        return f"GARRA:{GARRA_MAP[texto]}"
    return None

