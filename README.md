<h1 align="center">morte</h1>
<div align="center">
  <img src="orochinho.jpg" alt="" width="300">
</div>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Tkinter-GUI-blue?style=for-the-badge" alt="Tkinter">
</p>

> 🚨 **ALERTA DE PERIGO:** Este projeto contém altos níveis de zoeira, palavras suspeitas e verbos bizarros.

---

## 🕹️ O que é o "Morte"?

O **Morte** é a nossa versão "Orochinho Vibes" do famoso **Termo** (ou Wordle). O objetivo? Adivinhar a palavra secreta antes que o jogo te mate de raiva.

Você tem **6 tentativas** para acertar. Mas o jogo não facilita: ele sorteia palavras de três fontes diferentes (**palavras legais, palavras feias e verbos**). 

**Por que o nome "Morte"?** 
Porque quando o jogo te dá uma palavra impossível e você erra, a sua única reação é digitar... **M O R T E**. 💀

---

## 🧠 Como Jogar (As Regras)

O tabuleiro é **dinâmico**: ele se adapta ao tamanho da palavra secreta. Se tem 5 colunas, a palavra tem 5 letras. Se tem 9 colunas... boa sorte.

- 🟩 **Verde:** A letra tá certa no lugar certo.
- 🟨 **Amarelo:** A letra existe na palavra, mas tá no lugar errado.
- ⬛ **Cinza:** Essa letra aí não existe, mizeravi.

Digite pelo **teclado físico** do seu PC, aperte **Enter** para enviar e **Backspace** para apagar. Simples assim.

---

## 🛠️ O Cérebro por Trás do Caos

O projeto foi separado em duas partes (porque programador bom não mistura a bagunça):

- **`jogo.py`**: A lógica pura. Filtra as listas `.txt`, sorteia a palavra, checa as letras (com direito a tratamento especial para letras repetidas) e dita as regras.
- **`interface.py`**: A parte visual com **Tkinter**. Desenha os quadradinhos, escuta o teclado e faz o tabuleiro se adaptar ao tamanho da palavra.

---

## 🚀 Como invocar o "Morte" na sua máquina

1. Tenha o **Python 3** instalado.
2. Baixe a pasta do projeto e certifique-se de que os arquivos `.txt` estão na mesma pasta que os `.py`.
3. Abra o terminal e digite:
```bash
python interface.py
