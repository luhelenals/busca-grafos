import pandas as pd
import numpy as np
from classe_grafo import Grafo
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

def gerar_df_distancias():
    # Ler e formatar tabela de distâncias
    df = pd.read_excel(r'base_distancias_capitais.xlsx', index_col='Unnamed: 0')
    df.rename(columns={'R. Janeiro': 'Rio de Janeiro'}, inplace=True)
    df.index = df.columns
    
    arr_rodo = df.to_numpy()
    rows, cols = np.triu_indices_from(arr_rodo, k=-1) # Pegar índices da matriz triangular superior (distâncias aéreas)
    arr_rodo[rows, cols] = arr_rodo[cols, rows] # Espelhar para usar apenas distâncias rodoviárias

    arr_aereo = df.to_numpy()
    rows, cols = np.tril_indices_from(arr_aereo, k=-1) # Pegar índices da matriz triangular inferior (distâncias rodoviárias)
    arr_aereo[rows, cols] = arr_aereo[cols, rows] # Espelhar para usar apenas distâncias aéreas (estimando distâncias em linha reta)
    
    return pd.DataFrame(arr_rodo, index=df.index, columns=df.columns), pd.DataFrame(arr_aereo, index=df.index, columns=df.columns)

def criar_arestas(df, df_reta):
    # Dicionário de adjacências entre capitais (mapeadas pelo estado)
    estados_vizinhos = {
        'Rio Branco': ['Manaus', 'Porto Velho'],
        'Maceió': ['Salvador', 'Recife', 'Aracajú'],
        'Macapá': ['Belém'],
        'Manaus': ['Rio Branco', 'Porto Velho', 'Boa Vista', 'Belém', 'Cuiabá'],
        'Salvador': ['Maceió', 'Aracajú', 'Recife', 'Teresina', 'Goiânia', 'Belo Horizonte', 'Palmas', 'Vitória'],
        'Fortaleza': ['Natal', 'João Pessoa', 'Recife', 'Teresina'],
        'Brasília': ['Goiânia'],
        'Vitória': ['Salvador', 'Belo Horizonte', 'Rio de Janeiro'],
        'Goiânia': ['Cuiabá', 'Campo Grande', 'Belo Horizonte', 'Salvador', 'Palmas', 'Brasília'],
        'São Luis': ['Teresina', 'Palmas', 'Belém'],
        'Cuiabá': ['Porto Velho', 'Manaus', 'Belém', 'Palmas', 'Goiânia', 'Campo Grande'],
        'Campo Grande': ['Cuiabá', 'Goiânia', 'São Paulo', 'Belo Horizonte', 'Curitiba'],
        'Belo Horizonte': ['São Paulo', 'Rio de Janeiro', 'Vitória', 'Salvador', 'Goiânia', 'Campo Grande'],
        'Belém': ['Macapá', 'Manaus', 'Boa Vista', 'São Luis', 'Palmas', 'Cuiabá'],
        'João Pessoa': ['Natal', 'Fortaleza', 'Recife'],
        'Curitiba': ['Campo Grande', 'São Paulo', 'Florianópolis'],
        'Recife': ['Fortaleza', 'João Pessoa', 'Maceió', 'Salvador', 'Teresina'],
        'Teresina': ['Fortaleza', 'Recife', 'Salvador', 'Palmas', 'São Luis'],
        'Rio de Janeiro': ['Vitória', 'Belo Horizonte', 'São Paulo'],
        'Natal': ['Fortaleza', 'João Pessoa'],
        'Porto Velho': ['Rio Branco', 'Manaus', 'Cuiabá'],
        'Boa Vista': ['Manaus', 'Belém'],
        'Porto Alegre': ['Florianópolis'],
        'Florianópolis': ['Curitiba', 'Porto Alegre'],
        'Aracajú': ['Maceió', 'Salvador'],
        'São Paulo': ['Campo Grande', 'Belo Horizonte', 'Rio de Janeiro', 'Curitiba'],
        'Palmas': ['Belém', 'São Luis', 'Teresina', 'Salvador', 'Goiânia', 'Cuiabá']
    }

    arestas = set()

    for cidade, vizinhos in estados_vizinhos.items():
        for vizinho in vizinhos:
            aresta = tuple(sorted([cidade, vizinho])) # Ordenar para evitar duplicatas
            distancia = df.loc[aresta[0], aresta[1]] # Distância segundo o DF
            distancia_reta = df_reta.loc[aresta[0], aresta[1]] # Simulação de distância em linha reta
            peso_aresta = tuple((aresta[0], aresta[1], distancia, distancia_reta))
            arestas.add(peso_aresta)
    
    return arestas

def exibir_grafo(g):
    # Mapeamento de posições estimadas dos vértices do grafo de acordo com o mapa do Brasil
    pos = {
        'Rio Branco': (-0.5, 2.3),
        'Manaus': (1.3, 4.3),
        'Boa Vista': (0.5, 6),
        'Porto Velho': (1.5, 1.7),
        'Belém': (4.1, 4.5),
        'Macapá': (4.3, 6.2),
        'Palmas': (5.4, 3),
        'São Luis': (6, 4.5), 
        'Teresina': (7.2, 3.7), 
        'Fortaleza': (8.6, 4.5), 
        'Natal': (10.1, 4.8),
        'João Pessoa': (10.3, 3.6),
        'Recife': (9.5, 3),  
        'Maceió': (10, 2),  
        'Aracajú': (9.5, 1), 
        'Salvador': (8, 1), 
        'Cuiabá': (3.5, 0.7),
        'Campo Grande': (4, -2),
        'Goiânia': (5.3, 0.2),  
        'Brasília': (5.7, 1), 
        'Belo Horizonte': (6.7, -0.9),    
        'Vitória': (7.9, -1.5),  
        'Rio de Janeiro': (7.4, -3),  
        'São Paulo': (6.2, -3.7),
        'Curitiba': (5.6, -5.3),
        'Florianópolis': (5.5, -7),    
        'Porto Alegre': (4.9, -8.6),     
    }

    G = nx.Graph()

    # Adiciona arestas com o peso (distância)
    for origem, destinos in g._grafo.items():
        for destino, (distancia, _) in destinos.items():
            G.add_edge(origem, destino, weight=distancia, )

    # Desenha o grafo
    plt.figure(figsize=(16, 12))
    nx.draw(G, pos, with_labels=True, node_color='green', node_size=1000, font_size=8)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title("Grafo de Capitais do Brasil (com distâncias)")
    plt.axis('off')
    plt.show()

def mostrar_resultado(msg, titulo="Resultado"):
    # Janela nova
    top = tk.Toplevel()
    top.title(titulo)
    top.geometry("400x300")
    top.config(bg="#f0f0f0")

    # Título estilizado
    label_titulo = tk.Label(top, text=titulo, font=("Helvetica", 14, "bold"), bg="#f0f0f0")
    label_titulo.pack(pady=(10, 5))

    # Mensagem
    texto = tk.Text(top, wrap="word", bg="#ffffff", font=("Helvetica", 10), padx=10, pady=10)
    texto.insert("1.0", msg)
    texto.config(state="disabled", height=12, width=50)
    texto.pack(padx=10, pady=10)

    # Botão fechar
    botao = tk.Button(top, text="Fechar", command=top.destroy)
    botao.pack(pady=(0, 10))

def calcular_distancia(entrada_origem, entrada_destino, g):
    origem = entrada_origem.get()
    destino = entrada_destino.get()

    try:
        largura = g.busca_largura(origem, destino)
        profundidade = g.busca_profundidade(origem, destino)
        a_estrela = g.busca_a_estrela(origem, destino)

        msg = (
            f"☆ Busca em Largura:\n"
            f"→ Total de visitas = {len(largura[0])}\n"
            f"→ Rota: {largura[0]}\n"
            f"→ {largura[1]} km | {largura[2]} km (linha reta)\n\n"
            f"☆ Busca em Profundidade:\n"
            f"→ Total de visitas = {len(profundidade[0])}\n"
            f"→ Rota: {profundidade[0]}\n"
            f"→ {profundidade[1]} km | {profundidade[2]} km (linha reta)\n\n"
            f"☆ Busca A*:\n"
            f"→ Total de visitas = {len(a_estrela[0])}\n"
            f"→ Rota: {a_estrela[0]}\n"
            f"→ {a_estrela[1]} km | {a_estrela[2]} km (linha reta)"
        )

        mostrar_resultado(msg, f"Distância de {origem} para {destino}")
    
    except:
        messagebox.showinfo("Erro", "Entrada inválida")

def criar_janela(g):
    # Criar janela principal
    janela = tk.Tk()
    janela.title("Calculadora de Distância")
    janela.geometry("300x200")

    # Label e entrada para Capital Origem
    label_origem = tk.Label(janela, text="Capital Origem:")
    label_origem.pack(pady=(10, 0))
    entrada_origem = tk.Entry(janela)
    entrada_origem.pack()

    # Label e entrada para Capital Destino
    label_destino = tk.Label(janela, text="Capital Destino:")
    label_destino.pack(pady=(10, 0))
    entrada_destino = tk.Entry(janela)
    entrada_destino.pack()

    # Botão para Exibir Grafo
    botao_grafo = tk.Button(janela, text="Exibir Grafo", command=lambda: exibir_grafo(g))
    botao_grafo.pack(pady=(10, 0))

    # Botão para Calcular Distância
    botao_distancia = tk.Button(
        janela,
        text="Calcular Distância",
        command=lambda: calcular_distancia(entrada_origem, entrada_destino, g)
    )
    botao_distancia.pack(pady=(5, 0))

    # Iniciar o loop da interface
    janela.mainloop()

def main():
    df, df_reta = gerar_df_distancias()
    arestas = criar_arestas(df, df_reta)
    g = Grafo(connections=arestas)
    
    criar_janela(g)

if __name__ == '__main__':
    main()