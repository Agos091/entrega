import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import random
import time

# Funções para calcular as entregas e rotas
def calcular_tempo(origem, destino, matriz, indice_destinos):
    return matriz[indice_destinos[origem], indice_destinos[destino]]

# Algoritmo Básico para simular as entregas
def algoritmo_basico(destinos, matriz_conexoes, entregas):
    tempo_atual = 0
    lucro_total = 0
    origem = 'A'
    
    for entrega in entregas:
        tempo_inicio, destino, bonus = entrega
        tempo_desloc = calcular_tempo(origem, destino, matriz_conexoes, {d: i for i, d in enumerate(destinos)})
        tempo_retorno = calcular_tempo(destino, 'A', matriz_conexoes, {d: i for i, d in enumerate(destinos)})
        
        tempo_saida = max(tempo_atual, tempo_inicio)
        chegada = tempo_saida + tempo_desloc
        
        lucro_total += bonus
        tempo_atual = chegada + tempo_retorno
        origem = 'A'

    return lucro_total

# Função de Avaliação para o Algoritmo Genético
def avaliar_solucao(solucao, entregas, matriz_conexoes, indice_destinos):
    tempo_atual = 0
    lucro_total = 0
    origem = 'A'
    
    for entrega in solucao:
        tempo_inicio, destino, bonus = entrega
        tempo_desloc = calcular_tempo(origem, destino, matriz_conexoes, indice_destinos)
        tempo_retorno = calcular_tempo(destino, 'A', matriz_conexoes, indice_destinos)

        chegada = tempo_atual + tempo_desloc
        lucro_total += bonus
        tempo_atual = chegada + tempo_retorno
        origem = 'A'

    return lucro_total

# Algoritmo Genético
def algoritmo_genetico(entregas, matriz_conexoes, indice_destinos, num_geracoes=100, tamanho_populacao=20):
    # Criação da população inicial
    populacao = [random.sample(entregas, len(entregas)) for _ in range(tamanho_populacao)]
    
    for geracao in range(num_geracoes):
        # Avaliação da população
        avaliacoes = [avaliar_solucao(solucao, entregas, matriz_conexoes, indice_destinos) for solucao in populacao]
        
        # Seleção dos melhores indivíduos (elitismo)
        melhores = sorted(zip(populacao, avaliacoes), key=lambda x: x[1], reverse=True)[:tamanho_populacao // 2]
        
        nova_populacao = [solucao for solucao, avaliacao in melhores]
        
        # Cruzamento e Mutação
        while len(nova_populacao) < tamanho_populacao:
            pai1, pai2 = random.sample(melhores, 2)

            # Garantir que o tamanho da solução permita crossover
            if len(pai1[0]) > 1:
                ponto_corte = random.randint(1, len(pai1[0]) - 1)  # Corrigido ponto de corte
                filho = pai1[0][:ponto_corte] + pai2[0][ponto_corte:]
            else:
                filho = pai1[0]

            # Mutação
            if random.random() < 0.1:
                indice1, indice2 = random.sample(range(len(filho)), 2)
                filho[indice1], filho[indice2] = filho[indice2], filho[indice1]
            
            nova_populacao.append(filho)
        
        populacao = nova_populacao

    melhor_solucao, melhor_lucro = melhores[0]
    return melhor_solucao, melhor_lucro

# Função para exibir a simulação e logs
def simular_entregas(destinos, matriz_conexoes, entregas):
    indice_destinos = {d: i for i, d in enumerate(destinos)}
    
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

        # Frames para as seções da interface
        self.frame_destinos = tk.Frame(root)
        self.frame_conexoes = tk.Frame(root)
        self.frame_entregas = tk.Frame(root)
        self.frame_simulacao = tk.Frame(root)

        # Labels e entradas para Destinos
        tk.Label(self.frame_destinos, text="Adicionar Destinos").pack()
        self.destino_entry = tk.Entry(self.frame_destinos)
        self.destino_entry.pack()
        tk.Button(self.frame_destinos, text="Adicionar Destino", command=self.adicionar_destino).pack()

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

    # Adicionar destino
    def adicionar_destino(self):
        destino = self.destino_entry.get()
        if destino and destino not in self.destinos:
            self.destinos.append(destino)
            messagebox.showinfo("Destino", f"Destino {destino} adicionado.")
        else:
            messagebox.showwarning("Erro", "Destino inválido ou já existe.")

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

        if origem in self.destinos and destino in self.destinos:
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
        matriz_conexoes = np.zeros((num_destinos, num_destinos), dtype=int)

        # Criar matriz de conexões a partir das conexões adicionadas
        indice_destinos = {d: i for i, d in enumerate(self.destinos)}
        for origem, destino, tempo in self.conexoes:
            matriz_conexoes[indice_destinos[origem], indice_destinos[destino]] = tempo
            matriz_conexoes[indice_destinos[destino], indice_destinos[origem]] = tempo  # Bidirecional

        # Chamar a função de simulação
        simular_entregas(self.destinos, matriz_conexoes, self.entregas)

# Executar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
