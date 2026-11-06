import unicodedata
from pathlib import Path


def _normalizar_palavra(palavra):
    texto = unicodedata.normalize("NFD", palavra.upper().strip())
    texto = "".join(ch for ch in texto if unicodedata.category(ch) != "Mn")
    return texto


def carregar_txt(caminho):
    palavras = []
    with open(caminho, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            palavra = _normalizar_palavra(linha)
            if palavra:  # ignora linhas vazias
                palavras.append(palavra)
    return palavras



PASTA = Path(__file__).parent
lista1 = carregar_txt(PASTA / "palavrasfeias.txt")
lista2 = carregar_txt(PASTA / "palavraslegais.txt")
lista3 = carregar_txt(PASTA / "verbos.txt")


todas_as_palavras = list(set(lista1 + lista2 + lista3))


def _carregar_dicionario_portugues():
    caminhos = [
        "/usr/share/dict/words",
        "/usr/share/dict/portuguese",
        "/usr/share/dict/portugues",
        "/usr/share/dictionary/words",
        "/usr/share/dict/brazilian",
    ]

    dicionario = set()
    for caminho in caminhos:
        try:
            path = Path(caminho)
            if path.exists():
                with open(path, "r", encoding="utf-8", errors="ignore") as arquivo:
                    for linha in arquivo:
                        palavra = _normalizar_palavra(linha)
                        if palavra:
                            dicionario.add(palavra)
                if dicionario:
                    return dicionario
        except OSError:
            continue

    dicionario.update(_normalizar_palavra(p) for p in todas_as_palavras)
    return dicionario


DICIONARIO_PORTUGUES = _carregar_dicionario_portugues()


def palavra_valida(palavra):
    if not palavra:
        return False

    palavra_normalizada = _normalizar_palavra(palavra)
    if palavra_normalizada in DICIONARIO_PORTUGUES:
        return True

    try:
        from wordfreq import zipf_frequency
        frequencia = zipf_frequency(palavra_normalizada.lower(), "pt")
        return frequencia >= 2.0
    except Exception:
        return palavra_normalizada in {_normalizar_palavra(p) for p in todas_as_palavras}


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


