from pathlib import Path

def carregar_txt(caminho):
    palavras = []
    with open(caminho, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            palavra = linha.strip().upper()
            if palavra:  # ignora linhas vazias
                palavras.append(palavra)
    return palavras

def filtrar(palavras):
    # Aqui a gente filtra as de 5 letras
    validas = []
    for p in palavras:
        if len(p) == 5 and p.isalpha():
            validas.append(p)
    return validas

PASTA = Path(__file__).parent
lista1 = carregar_txt(PASTA / "palavaasfeias.txt")
lista2 = carregar_txt(PASTA / "palavaaslegais.txt")
lista3 = carregar_txt(PASTA / "verbos.txt")

feias_filtradas = filtrar(lista1)
verbos_filtrados = filtrar(lista3)

todas_as_palavras = list(set(feias_filtradas + verbos_filtrados + lista2))

def sortear_palavra():
    import random
    secreta = random.choice(todas_as_palavras)

    return secreta

def checar_palpite(palpite, secreta):
    # Lista que vai guardar as cores finais (ex: ["verde", "cinza", "amarelo"...])
    resultado = [None] * len(secreta)

    # Marca primeiro as letras na posição correta.
    letras_secretas = list(secreta)
    for i in range(len(secreta)):
        if palpite[i] == secreta[i]:
            resultado[i] = "verde"
            letras_secretas[i] = None

    # Marca letras presentes na palavra secreta, sem contar duplicatas além do disponível.
    for i in range(len(secreta)):
        if resultado[i] is None:
            letra = palpite[i]
            if letra in letras_secretas:
                resultado[i] = "amarelo"
                index_usado = letras_secretas.index(letra)
                letras_secretas[index_usado] = None
            else:
                resultado[i] = "cinza"

    return resultado


