import numpy as np
import matplotlib.pyplot as plt
import time

# Matriz de conexões entre destinos (A, B, C, D)
conexoes = np.array([
    [0, 5, 0, 2],  # A
    [5, 0, 3, 0],  # B
    [0, 3, 0, 8],  # C
    [2, 0, 8, 0]   # D
])

# Lista de entregas: (tempo de início, destino, bônus)
entregas = [
    (0, 'B', 1),
    (5, 'C', 10),
    (10, 'D', 8)
]

# Mapeia letras para índices da matriz de conexões
letras_para_indices = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
indices_para_letras = {v: k for k, v in letras_para_indices.items()}

# Função para calcular o tempo de deslocamento entre dois destinos
def tempo_deslocamento(origem, destino, matriz_conexoes):
    return matriz_conexoes[letras_para_indices[origem], letras_para_indices[destino]]

# Função para processar as entregas sem otimização
def processar_entregas(entregas, matriz_conexoes):
    lucro_total = 0
    tempo_atual = 0
    rota = []
    origem = 'A'
    
    for entrega in entregas:
        tempo_inicio, destino, bonus = entrega
        tempo_necessario = tempo_deslocamento(origem, destino, matriz_conexoes)
        
        # Se a entrega pode ser feita no tempo correto
        if tempo_atual + tempo_necessario <= tempo_inicio:
            rota.append(destino)
            lucro_total += bonus
            tempo_atual += tempo_necessario
        else:
            print(f"Entrega para {destino} não pode ser realizada no tempo!")
        
        origem = destino  # Atualiza o ponto de origem

    return rota, lucro_total

# Função para exibir os resultados
def exibir_resultados(rota, lucro_total):
    print("Sequência de entregas realizadas:", ' -> '.join(rota))
    print(f"Lucro esperado: {lucro_total}")

# Função para medir o desempenho de execução
def medir_desempenho(funcao, *args):
    inicio = time.time()
    resultado = funcao(*args)
    fim = time.time()
    tempo_execucao = fim - inicio
    return resultado, tempo_execucao

# Processa e exibe os resultados
rota, lucro_total = processar_entregas(entregas, conexoes)
exibir_resultados(rota, lucro_total)
