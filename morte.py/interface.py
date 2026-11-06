import tkinter as tk
from tkinter import messagebox

import jogo

CORES = {
    "verde": "#4CAF50",
    "amarelo": "#F4C542",
    "cinza": "#3A3A3C",
    "padrao": "#1F1F21",
    "teclado": "#787C7E",
}

TECLADO_LAYOUT = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M"],
]


class JogoMorte:
    def __init__(self, janela):
        self.janela = janela
        self.secreta = jogo.sortear_palavra()
        self.tamanho = len(self.secreta)
        self.max_tentativas = 6
        self.palpite_atual = []
        self.tentativas = []
        self.celulas = []
        self.estado_teclas = {}
        self.botoes_teclado = {}
        self.indice_selecionado = 0

        self._montar_interface()
        self._criar_tabuleiro()
        self._criar_teclado()
        self._ajustar_tamanho_janela()
        self._atualizar_linha_ativa()
        self._atualizar_teclado()

        self.janela.bind("<Key>", self._on_tecla)
        self.janela.bind("<BackSpace>", lambda evento: self._apagar())
        self.janela.bind("<Return>", lambda evento: self._enviar())

    def _montar_interface(self):
        self.janela.title("morte")
        self.janela.configure(bg="#121213")
        self.janela.resizable(False, False)

        titulo = tk.Label(
            self.janela,
            text="morte",
            fg="white",
            bg="#121213",
            font=("Arial", 24, "bold"),
        )
        titulo.pack(pady=(20, 10))

        self.status = tk.StringVar(value=f"A palavra tem {self.tamanho} letras")
        status_label = tk.Label(
            self.janela,
            textvariable=self.status,
            fg="#D7D7D7",
            bg="#121213",
            font=("Arial", 11),
        )
        status_label.pack(pady=(0, 12))

        self.tabuleiro = tk.Frame(self.janela, bg="#121213")
        self.tabuleiro.pack()

        self.teclado_frame = tk.Frame(self.janela, bg="#121213")
        self.teclado_frame.pack(pady=(20, 10))

    def _criar_tabuleiro(self):
        for linha in range(self.max_tentativas):
            elementos = []
            for coluna in range(self.tamanho):
                celula = tk.Label(
                    self.tabuleiro,
                    text="",
                    width=4,
                    height=2,
                    bg=CORES["padrao"],
                    fg="white",
                    font=("Arial", 20, "bold"),
                    borderwidth=2,
                    relief="solid",
                    padx=8,
                    pady=8,
                    highlightthickness=2,
                    highlightbackground="#3A3A3C",
                    cursor="hand2",
                )
                celula.grid(row=linha, column=coluna, padx=8, pady=8)
                celula.bind("<Button-1>", lambda evento, linha=linha, coluna=coluna: self._selecionar_celula(linha, coluna))
                elementos.append(celula)
            self.celulas.append(elementos)

    def _ajustar_tamanho_janela(self):
        self.janela.update_idletasks()

        largura_tabuleiro = self.tabuleiro.winfo_reqwidth()
        altura_tabuleiro = self.tabuleiro.winfo_reqheight()
        altura_teclado = self.teclado_frame.winfo_reqheight()

        margem_horizontal = 60
        margem_vertical = 120

        largura = max(500, largura_tabuleiro + margem_horizontal)
        altura = altura_tabuleiro + altura_teclado + margem_vertical

        self.janela.geometry(f"{largura}x{altura}")

    def _criar_teclado(self):
        for linha in TECLADO_LAYOUT:
            linha_frame = tk.Frame(self.teclado_frame, bg="#121213")
            linha_frame.pack(pady=4)

            for letra in linha:
                botao = tk.Button(
                    linha_frame,
                    text=letra,
                    width=4,
                    height=2,
                    bg=CORES["teclado"],
                    fg="white",
                    font=("Arial", 11, "bold"),
                    relief="flat",
                    bd=0,
                    command=lambda l=letra: self._tecla_virtual(l),
                )
                botao.pack(side=tk.LEFT, padx=3)
                self.botoes_teclado[letra] = botao

        botoes_acoes = tk.Frame(self.teclado_frame, bg="#121213")
        botoes_acoes.pack(pady=6)

        botao_apagar = tk.Button(
            botoes_acoes,
            text="⌫",
            width=6,
            height=2,
            bg="#2A2A2D",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            command=lambda: self._apagar(),
        )
        botao_apagar.pack(side=tk.LEFT, padx=4)

        botao_enviar = tk.Button(
            botoes_acoes,
            text="ENTER",
            width=8,
            height=2,
            bg="#2A2A2D",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            command=lambda: self._enviar(),
        )
        botao_enviar.pack(side=tk.LEFT, padx=4)

        self.botoes_teclado["⌫"] = botao_apagar
        self.botoes_teclado["ENTER"] = botao_enviar

    def _selecionar_celula(self, linha, coluna):
        if linha != len(self.tentativas):
            return
        if 0 <= coluna < self.tamanho:
            self.indice_selecionado = coluna
            self.janela.focus_set()
            self._atualizar_linha_ativa()

    def _atualizar_linha_ativa(self):
        linha_atual = len(self.tentativas)
        for index in range(self.tamanho):
            celula = self.celulas[linha_atual][index]
            if index < len(self.palpite_atual):
                celula.config(text=self.palpite_atual[index], bg=CORES["padrao"])
            else:
                celula.config(text="", bg=CORES["padrao"])

            if index == self.indice_selecionado and linha_atual == len(self.tentativas):
                celula.config(highlightthickness=3, highlightbackground="#FFFFFF")
            else:
                celula.config(highlightthickness=2, highlightbackground="#3A3A3C")

    def _atualizar_teclado(self):
        for letra, botao in self.botoes_teclado.items():
            if letra in {"⌫", "ENTER"}:
                continue
            estado = self.estado_teclas.get(letra)
            if estado == "verde":
                cor = CORES["verde"]
            elif estado == "amarelo":
                cor = CORES["amarelo"]
            elif estado == "cinza":
                cor = CORES["cinza"]
            else:
                cor = CORES["teclado"]
            botao.config(bg=cor, fg="white")

    def _adicionar_letra(self, letra):
        while len(self.palpite_atual) < self.tamanho:
            self.palpite_atual.append("")

        if self.indice_selecionado >= self.tamanho:
            self.indice_selecionado = self.tamanho - 1

        self.palpite_atual[self.indice_selecionado] = letra

        if self.indice_selecionado < self.tamanho - 1:
            self.indice_selecionado += 1

        self._atualizar_linha_ativa()
        self.status.set(f"Tentativa {len(self.tentativas) + 1}: {''.join(self.palpite_atual)}")

    def _tecla_virtual(self, letra):
        if len(self.tentativas) >= self.max_tentativas:
            return
        self._adicionar_letra(letra)

    def _on_tecla(self, evento):
        if len(self.tentativas) >= self.max_tentativas:
            return
        if evento.char and evento.char.isalpha():
            letra = evento.char.upper()
            self._adicionar_letra(letra)

    def _apagar(self, evento=None):
        if len(self.tentativas) >= self.max_tentativas:
            return

        while len(self.palpite_atual) < self.tamanho:
            self.palpite_atual.append("")

        if self.indice_selecionado >= 0 and self.indice_selecionado < self.tamanho:
            self.palpite_atual[self.indice_selecionado] = ""

        while self.palpite_atual and self.palpite_atual[-1] == "":
            self.palpite_atual.pop()

        self.indice_selecionado = min(self.indice_selecionado, max(0, len(self.palpite_atual) - 1))

        self._atualizar_linha_ativa()
        self.status.set(f"Tentativa {len(self.tentativas) + 1}: {''.join(self.palpite_atual)}")

    def _registrar_resultado_teclado(self, palpite, resultado):
        for indice, estado in enumerate(resultado):
            letra = palpite[indice]
            atual = self.estado_teclas.get(letra)

            if estado == "verde":
                self.estado_teclas[letra] = "verde"
            elif estado == "amarelo" and atual != "verde":
                self.estado_teclas[letra] = "amarelo"
            elif estado == "cinza" and atual not in {"verde", "amarelo"}:
                self.estado_teclas[letra] = "cinza"

        self._atualizar_teclado()

    def _enviar(self, evento=None):
        if len(self.palpite_atual) != self.tamanho:
            self.status.set(f"Digite exatamente {self.tamanho} letras.")
            return

        palpite = "".join(self.palpite_atual)
        if not jogo.palavra_valida(palpite):
            self.status.set(f"'{palpite}' não é uma palavra válida do português.")
            messagebox.showerror("morte", f"'{palpite}' não está no dicionário do português.")
            return

        resultado = jogo.checar_palpite(palpite, self.secreta)

        linha_atual = len(self.tentativas)
        for indice, cor in enumerate(resultado):
            celula = self.celulas[linha_atual][indice]
            celula.config(
                text=self.palpite_atual[indice],
                bg=CORES[cor],
                fg="white",
            )

        self._registrar_resultado_teclado(palpite, resultado)
        self.tentativas.append(palpite)

        if palpite == self.secreta:
            self.status.set(f"Você venceu! A palavra era {self.secreta}.")
            messagebox.showinfo("morte", f"Você acertou! A palavra era {self.secreta}.")
            self.janela.unbind("<Key>")
            self.janela.unbind("<BackSpace>")
            self.janela.unbind("<Return>")
            return

        if len(self.tentativas) >= self.max_tentativas:
            self.status.set(f"A palavra era {self.secreta}.")
            messagebox.showinfo("morte", f"A palavra era {self.secreta}.")
            self.janela.unbind("<Key>")
            self.janela.unbind("<BackSpace>")
            self.janela.unbind("<Return>")
            return

        self.palpite_atual = []
        self._atualizar_linha_ativa()
        self.status.set(f"Próxima tentativa: {len(self.tentativas) + 1}/{self.max_tentativas}")


if __name__ == "__main__":
    janela = tk.Tk()
    app = JogoMorte(janela)
    janela.mainloop()