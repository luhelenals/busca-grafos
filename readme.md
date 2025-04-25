# 🧭 Algoritmos de Busca em Grafos - Capitais do Brasil

Como primeiro trabalho da disciplina de Inteligência Artificial, foi elaborado um trabalho para prática de algoritmos de busca em grafos. Este projeto implementa uma estrutura de grafo para representar conexões entre capitais brasileiras, utilizando distâncias rodoviárias e aéreas como pesos e heurísticas, respectivamente. São implementadas as buscas em profundidade, largura e A* (A-estrela), com base em dados reais de distâncias.

## 📦 Estrutura do Projeto

- `classe_grafo.py`: Classe `Grafo`, com métodos para adicionar conexões e executar os algoritmos de busca.
- `base_distancias_capitais.xlsx`: Planilha contendo as distâncias entre capitais.
- `main.py`: Script principal que manipula os dados, monta o grafo e executa os algoritmos.
- Utiliza bibliotecas como `pandas`, `numpy`, `tkinter` (GUI) e `networkx` + `matplotlib` (visualização do grafo).

## 🚀 Funcionalidades

- Criação dinâmica do grafo com base em dados da planilha.
- Implementação dos algoritmos de:
  - Busca em Profundidade (DFS)
  - Busca em Largura (BFS)
  - Busca A* (A-estrela)
- Visualização gráfica do grafo representando as capitais e conexões.
- Interface gráfica simples usando `tkinter`.

## 🧠 Algoritmos de Busca

### 🔎 Busca em Profundidade (DFS)
Percorre recursivamente os nós, explorando o mais longe possível antes de retroceder.

### 🔄 Busca em Largura (BFS)
Percorre o grafo camada por camada, ideal para encontrar o caminho mais curto em grafos não ponderados.

### ⭐ A* (A-estrela)
Algoritmo heurístico que combina o custo já percorrido com uma estimativa (distância em linha reta) do que ainda falta.

## 📊 Dados

Os dados de distância são carregados de uma planilha Excel contendo:
- Distâncias rodoviárias (usadas como peso real das arestas).
- Estimativas de distâncias em linha reta (usadas como heurística para o A*).

## 📈 Visualização

O grafo é renderizado com `networkx` e `matplotlib`, com as capitais posicionadas de forma aproximada geograficamente.

## 🛠️ Como Executar

1. Instale as dependências:
```bash
pip install pandas numpy networkx matplotlib openpyxl
```
2. Coloque o arquivo base_distancias_capitais.xlsx na raiz do projeto.
3. Execute o script principal:
```bash
python main.py
```

## 🔎 Fontes do Trabalho
- [Pathfinding para iniciantes](https://www.inf.ufsc.br/~alexandre.goncalves.silva/courses/14s2/ine5633/trabalhos/t1/A%20%20%20Pathfinding%20para%20Iniciantes.pdf)
- [Documentação NewtworkX](https://networkx.org/documentation/stable/tutorial.html)
- [Mapa de Adjacências entre Estados](https://www.researchgate.net/figure/Figura-13-Adjacncia-entre-estados-do-Brasil-veja-exemplo-15_fig1_327057443)
- [Distâncias Entre as Capitais Brasileiras](https://www.goodway.com.br/distancias.htm)

## 📚 Reursos Úteis
- [VisualGo](https://visualgo.net/) (Visualização de estruturas de dados)
- [Algoritmos - Thomas Cormen](https://computerscience360.wordpress.com/wp-content/uploads/2018/02/algoritmos-teoria-e-prc3a1tica-3ed-thomas-cormen.pdf) (Livro de introdução a Algoritmos)
