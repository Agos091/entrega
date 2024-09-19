import numpy as np
import random
import os

# Funções de leitura da matriz de conexões e lista de entregas
def ler_matriz_conexoes(caminho_arquivo):
    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()
    num_destinos = int(linhas[0].strip())
    destinos = [dest.strip() for dest in linhas[1].split(',')]
    matriz = []
    for linha in linhas[2:2 + num_destinos]:
        tempos = [int(x.strip()) for x in linha.split(',')]
        matriz.append(tempos)
    matriz = np.array(matriz)
    return destinos, matriz

def ler_lista_entregas(caminho_arquivo):
    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()
    num_entregas = int(linhas[0].strip())
    entregas = []
    for linha in linhas[1:1 + num_entregas]:
        partes = [parte.strip() for parte in linha.split(',')]
        tempo_inicio = int(partes[0])
        destino = partes[1]
        bonus = int(partes[2])
        entregas.append((tempo_inicio, destino, bonus))
    return entregas

# Função para calcular o tempo de deslocamento entre destinos
def calcular_tempo(origem, destino, matriz, indice_destinos):
    return matriz[indice_destinos[origem], indice_destinos[destino]]

# Função de avaliação do GA (calcula o lucro total de uma solução)
def avaliar_solucao(solucao, entregas, matriz_conexoes, indice_destinos):
    tempo_atual = 0
    lucro_total = 0
    origem = 'A'
    
    for entrega in solucao:
        tempo_inicio, destino, bonus = entrega
        tempo_desloc = calcular_tempo(origem, destino, matriz_conexoes, indice_destinos)
        tempo_retorno = calcular_tempo(destino, 'A', matriz_conexoes, indice_destinos)
        tempo_total_viagem = tempo_desloc + tempo_retorno

        chegada = tempo_atual + tempo_desloc
        retorno = chegada + tempo_retorno
        
        # Se a entrega puder ser realizada a tempo, acumula o lucro
        if chegada <= tempo_inicio:
            lucro_total += bonus
            tempo_atual = retorno
            origem = 'A'  # Sempre volta para A após cada entrega
    
    return lucro_total

# Função de crossover (cruza duas soluções para gerar uma nova)
def crossover(pai1, pai2):
    ponto_corte = random.randint(1, len(pai1) - 2)
    filho = pai1[:ponto_corte] + pai2[ponto_corte:]
    return filho

# Função de mutação (muda aleatoriamente um destino da rota)
def mutacao(solucao):
    indice1, indice2 = random.sample(range(len(solucao)), 2)
    solucao[indice1], solucao[indice2] = solucao[indice2], solucao[indice1]
    return solucao

# Algoritmo Genético
def algoritmo_genetico(entregas, matriz_conexoes, indice_destinos, num_geracoes=100, tamanho_populacao=20):
    # Criação da população inicial (soluções aleatórias)
    populacao = [random.sample(entregas, len(entregas)) for _ in range(tamanho_populacao)]
    
    for geracao in range(num_geracoes):
        # Avaliação da população
        avaliacoes = [avaliar_solucao(solucao, entregas, matriz_conexoes, indice_destinos) for solucao in populacao]
        
        # Seleção dos melhores indivíduos (elitismo)
        melhores = sorted(zip(populacao, avaliacoes), key=lambda x: x[1], reverse=True)[:tamanho_populacao // 2]
        
        nova_populacao = [solucao for solucao, avaliacao in melhores]
        
        # Cruzamento para gerar nova população
        while len(nova_populacao) < tamanho_populacao:
            pai1, pai2 = random.sample(melhores, 2)
            filho = crossover(pai1[0], pai2[0])
            
            # Aplica mutação com pequena probabilidade
            if random.random() < 0.1:
                filho = mutacao(filho)
            
            nova_populacao.append(filho)
        
        populacao = nova_populacao
        
        # Exibir os melhores resultados de cada geração
        melhor_solucao, melhor_lucro = melhores[0]
        print(f"Geração {geracao + 1}: Melhor lucro = {melhor_lucro}")
    
    return melhor_solucao, melhor_lucro

def versao2(diretorio_dados):
    # Caminhos dos arquivos
    caminho_conexoes = os.path.join(diretorio_dados, 'conexoes.txt')
    caminho_entregas = os.path.join(diretorio_dados, 'entregas.txt')
    
    # Ler dados
    destinos, matriz_conexoes = ler_matriz_conexoes(caminho_conexoes)
    entregas = ler_lista_entregas(caminho_entregas)
    
    # Mapear letras para índices
    indice_destinos = {destino: idx for idx, destino in enumerate(destinos)}
    
    # Executar o algoritmo genético
    melhor_solucao, melhor_lucro = algoritmo_genetico(entregas, matriz_conexoes, indice_destinos)
    
    # Exibir a melhor solução
    print("\nMelhor sequência de entregas:")
    for entrega in melhor_solucao:
        tempo_inicio, destino, bonus = entrega
        print(f"Entrega: Destino {destino}, Bônus {bonus}, Horário de início {tempo_inicio}")
    print(f"\nMelhor lucro obtido: {melhor_lucro}")

if __name__ == "__main__":
    # Defina o diretório onde estão os arquivos de dados
    diretorio_dados = os.path.join(os.getcwd(), 'dados')
    versao2(diretorio_dados)
