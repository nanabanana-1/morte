import tkinter as tk
import jogo
import random

# Cria a janela principal
janela = tk.Tk()
janela.title("morte")
janela.geometry("400x600") # Largura x Altura
janela.configure(bg="#121213") # Cor de fundo escura igual do Wordle

# Cria um texto qualquer pra testar
titulo = tk.Label(janela, text="morte", fg="white", bg="#121213", font=("Arial", 24, "bold"))
titulo.pack(pady=20)

# Roda a janela (isso tem que ficar no final)
janela.mainloop()