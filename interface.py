import tkinter as tk
from tkinter import messagebox
import random
import numpy as np
import time

# Algoritmo Básico
def algoritmo_basico(destinos, matriz_conexoes, entregas):
    # Implementação do algoritmo básico
    return random.randint(100, 1000)  # Exemplo de retorno de lucro aleatório

# Algoritmo Genético
def algoritmo_genetico(entregas, matriz_conexoes, indice_destinos):
    # Implementação do algoritmo genético
    return None, random.randint(100, 1000)  # Exemplo de retorno de lucro aleatório

# Função de simulação
def simular_entregas(destinos, matriz_conexoes, entregas, indice_destinos):
    # Algoritmo Básico
    start_basico = time.time()
    lucro_basico = algoritmo_basico(destinos, matriz_conexoes, entregas)
    tempo_basico = time.time() - start_basico
    
    # Algoritmo Genético
    start_genetico = time.time()
    _, lucro_genetico = algoritmo_genetico(entregas, matriz_conexoes, indice_destinos)
    tempo_genetico = time.time() - start_genetico
    
    # Logs para comparação
    print("---- Comparação de Resultados ----")
    print(f"Algoritmo Básico: Lucro = {lucro_basico}, Tempo = {tempo_basico:.4f} segundos")
    print(f"Algoritmo Genético: Lucro = {lucro_genetico}, Tempo = {tempo_genetico:.4f} segundos")
    
    # Mostrar resultados em uma mensagem
    messagebox.showinfo("Resultados da Simulação",
                        f"Algoritmo Básico:\nLucro = {lucro_basico}\nTempo = {tempo_basico:.4f} segundos\n\n"
                        f"Algoritmo Genético:\nLucro = {lucro_genetico}\nTempo = {tempo_genetico:.4f} segundos")

# Interface gráfica para adicionar conexões e entregas
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Leilão de Entregas")
        
        self.destinos = []
        self.conexoes = []
        self.entregas = []
        self.entry_points = []

        # Frames para as seções da interface
        self.frame_destinos = tk.Frame(root)
        self.frame_conexoes = tk.Frame(root)
        self.frame_entregas = tk.Frame(root)
        self.frame_simulacao = tk.Frame(root)

        # Labels e entradas para Destinos
        tk.Label(self.frame_destinos, text="Número de Destinos").pack()
        self.num_destinos_entry = tk.Entry(self.frame_destinos)
        self.num_destinos_entry.pack()
        
        # Labels e entradas para Pontos de Entrada
        tk.Label(self.frame_destinos, text="Número de Pontos de Entrada").pack()
        self.num_entry_points_entry = tk.Entry(self.frame_destinos)
        self.num_entry_points_entry.pack()
        
        tk.Button(self.frame_destinos, text="Gerar Destinos e Pontos de Entrada", command=self.gerar_destinos).pack()

        # Labels e entradas para Conexões
        tk.Label(self.frame_conexoes, text="Adicionar Conexões (Origem, Destino, Tempo) inserir um por input").pack()
        self.origem_entry = tk.Entry(self.frame_conexoes)
        self.origem_entry.pack()
        self.destino_conexao_entry = tk.Entry(self.frame_conexoes)
        self.destino_conexao_entry.pack()
        self.tempo_conexao_entry = tk.Entry(self.frame_conexoes)
        self.tempo_conexao_entry.pack()
        tk.Button(self.frame_conexoes, text="Adicionar Conexão", command=self.adicionar_conexao).pack()

        # Adicionar Listbox para exibir as conexões
        tk.Label(self.frame_conexoes, text="Conexões Adicionadas").pack()
        self.lista_conexoes = tk.Listbox(self.frame_conexoes, height=5, width=40)
        self.lista_conexoes.pack()

        # Labels e entradas para Entregas
        tk.Label(self.frame_entregas, text="Adicionar Entregas (Tempo, Destino, Bônus)").pack()
        self.tempo_entrega_entry = tk.Entry(self.frame_entregas)
        self.tempo_entrega_entry.pack()
        self.destino_entrega_entry = tk.Entry(self.frame_entregas)
        self.bonus_entrega_entry = tk.Entry(self.frame_entregas)
        self.destino_entrega_entry.pack()
        self.bonus_entrega_entry.pack()
        tk.Button(self.frame_entregas, text="Adicionar Entrega", command=self.adicionar_entrega).pack()

        # Botão para iniciar simulação
        tk.Button(self.frame_simulacao, text="Iniciar Simulação", command=self.iniciar_simulacao).pack()

        # Layout dos frames
        self.frame_destinos.pack(pady=10)
        self.frame_conexoes.pack(pady=10)
        self.frame_entregas.pack(pady=10)
        self.frame_simulacao.pack(pady=10)

    # Gerar destinos e conexões aleatórias
    def gerar_destinos(self):
        try:
            num_destinos = int(self.num_destinos_entry.get())
            num_entry_points = int(self.num_entry_points_entry.get())
            if num_destinos <= 0 or num_entry_points <= 0:
                raise ValueError("O número de destinos e pontos de entrada deve ser positivo.")
        except ValueError:
            messagebox.showwarning("Erro", "Número de destinos ou pontos de entrada inválido. Insira um número positivo.")
            return

        self.destinos = [chr(65 + i) for i in range(num_destinos)]  # Gerar destinos A, B, C, ...
        self.entry_points = [f"EP{i+1}" for i in range(num_entry_points)]  # Gerar pontos de entrada EP1, EP2, ...
        self.conexoes = []

        for i in range(num_destinos):
            for j in range(i + 1, num_destinos):
                tempo = random.randint(1, 20)  # Gerar tempos aleatórios entre 1 e 20 minutos
                self.conexoes.append((self.destinos[i], self.destinos[j], tempo))
                self.lista_conexoes.insert(tk.END, f"{self.destinos[i]} -> {self.destinos[j]}: {tempo} min")
                self.lista_conexoes.insert(tk.END, f"{self.destinos[j]} -> {self.destinos[i]}: {tempo} min")

        for ep in self.entry_points:
            for destino in self.destinos:
                tempo = random.randint(1, 20)  # Gerar tempos aleatórios entre 1 e 20 minutos
                self.conexoes.append((ep, destino, tempo))
                self.lista_conexoes.insert(tk.END, f"{ep} -> {destino}: {tempo} min")
                self.lista_conexoes.insert(tk.END, f"{destino} -> {ep}: {tempo} min")

        messagebox.showinfo("Destinos e Conexões", f"{num_destinos} destinos, {num_entry_points} pontos de entrada e conexões aleatórias gerados.")

    # Adicionar conexão e exibir na lista
    def adicionar_conexao(self):
        origem = self.origem_entry.get()
        destino = self.destino_conexao_entry.get()
        try:
            tempo = int(self.tempo_conexao_entry.get())
            if tempo <= 0:
                raise ValueError("O tempo de conexão deve ser positivo.")
        except ValueError:
            messagebox.showwarning("Erro", "Tempo de conexão inválido. Insira um número positivo.")
            return

        if (origem in self.destinos or origem in self.entry_points) and (destino in self.destinos or destino in self.entry_points):
            self.conexoes.append((origem, destino, tempo))
            self.lista_conexoes.insert(tk.END, f"{origem} -> {destino}: {tempo} min")
            messagebox.showinfo("Conexão", f"Conexão {origem} -> {destino} adicionada com tempo {tempo}.")
        else:
            messagebox.showwarning("Erro", "Origem ou destino inválido.")

    # Adicionar entrega
    def adicionar_entrega(self):
        try:
            tempo = int(self.tempo_entrega_entry.get())
        except ValueError:
            messagebox.showwarning("Erro", "Tempo de entrega inválido.")
            return

        destino = self.destino_entrega_entry.get()
        try:
            bonus = int(self.bonus_entrega_entry.get())
        except ValueError:
            messagebox.showwarning("Erro", "Bônus inválido.")
            return

        if destino in self.destinos:
            self.entregas.append((tempo, destino, bonus))
            messagebox.showinfo("Entrega", f"Entrega para {destino} adicionada no tempo {tempo} com bônus {bonus}.")
        else:
            messagebox.showwarning("Erro", "Destino inválido.")

    # Iniciar simulação
    def iniciar_simulacao(self):
        if not self.destinos or not self.conexoes or not self.entregas:
            messagebox.showwarning("Erro", "É necessário adicionar destinos, conexões e entregas.")
            return
        
        num_destinos = len(self.destinos)
        num_entry_points = len(self.entry_points)
        total_points = num_destinos + num_entry_points
        matriz_conexoes = np.zeros((total_points, total_points), dtype=int)

        # Criar matriz de conexões a partir das conexões adicionadas
        indice_destinos = {d: i for i, d in enumerate(self.destinos + self.entry_points)}
        for origem, destino, tempo in self.conexoes:
            matriz_conexoes[indice_destinos[origem], indice_destinos[destino]] = tempo
            matriz_conexoes[indice_destinos[destino], indice_destinos[origem]] = tempo  # Bidirecional

        # Chamar a função de simulação
        simular_entregas(self.destinos + self.entry_points, matriz_conexoes, self.entregas, indice_destinos)

    # Gerar entradas aleatórias
    def gerar_entradas_aleatorias(self):
        num_destinos = random.randint(5, 10)  # Número aleatório de destinos entre 5 e 10
        num_entry_points = random.randint(1, 5)  # Número aleatório de pontos de entrada entre 1 e 5
        self.num_destinos_entry.delete(0, tk.END)
        self.num_destinos_entry.insert(0, str(num_destinos))
        self.num_entry_points_entry.delete(0, tk.END)
        self.num_entry_points_entry.insert(0, str(num_entry_points))
        self.gerar_destinos()

        num_entregas = random.randint(5, 15)  # Número aleatório de entregas entre 5 e 15
        for _ in range(num_entregas):
            tempo = random.randint(1, 100)
            destino = random.choice(self.destinos)
            bonus = random.randint(10, 100)
            self.entregas.append((tempo, destino, bonus))
            self.lista_conexoes.insert(tk.END, f"Entrega: Tempo={tempo}, Destino={destino}, Bônus={bonus}")

        messagebox.showinfo("Entradas Aleatórias", "Entradas aleatórias geradas com sucesso.")

# Executar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    tk.Button(root, text="Gerar Entradas Aleatórias", command=app.gerar_entradas_aleatorias).pack(pady=10)
    root.mainloop()