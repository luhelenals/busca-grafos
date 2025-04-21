import pprint
from collections import defaultdict
from collections import deque

class Grafo(object):
    def __init__(self, connections):
        self._grafo = defaultdict(dict)
        self.add_conexao(connections)

    def add_conexao(self, connections):
        for node1, node2, peso, h in connections:
            self.add(node1, node2, peso, h)

    def add(self, node1, node2, peso, h):
        self._grafo[node1][node2] = (peso, h)
        self._grafo[node2][node1] = (peso, h)

    def busca_profundidade(self, node1, node2, path=[], peso=0, h=0):
        # Adiciona o primeiro nó ao caminho
        path = path + [node1]

        # Caso tenha encontrado o nó, retorna o caminho, soma dos pesos e heurísticas
        if node1 == node2:
            return path, peso, h
        
        # Retorna None se o primeiro nó não estiver no grafo
        if node1 not in self._grafo:
            return None
        
        # Para cada vizinho não visitado, chama a função recursivamente
        for vizinho in self._grafo[node1]:
            if vizinho not in path:
                # Soma dos pesos e heurísticas
                peso_aresta = self._grafo[node1][vizinho][0]
                h_aresta = self._grafo[node1][vizinho][1]
                
                result = self.busca_profundidade(vizinho, node2, path, peso + peso_aresta, h + h_aresta)
                if result:
                    return result
        return None

    def busca_largura(self, start, goal):
        # Fila com o nó inicial
        lista = deque([([start], 0, 0)])
        visitado = set()

        while lista:
            path, total_peso, total_h = lista.popleft()
            node = path[-1]

            # Caso encontre o nó desejado, retorna o caminho e soma dos pesos e heurísticas
            if node == goal:
                return path, total_peso, total_h
            
            # Se o nó não foi visitado, adiciona-o à lista de visitados
            if node not in visitado:
                visitado.add(node)

                # Para cada vizinho dele, adiciona este à *fila* caso já não esteja
                for vizinho in self._grafo[node]:
                    if vizinho not in path:
                        new_path = list(path)
                        new_path.append(vizinho)
                        new_peso = total_peso + self._grafo[node][vizinho][0]
                        new_h = total_h + self._grafo[node][vizinho][1]
                        lista.append((new_path, new_peso, new_h))
        return None

    def busca_a_estrela(self, start, goal):
        aberta = [(start, 0, 0, 0, [])]  # (nó, F, G, H, caminho)
        fechada = []

        while len(aberta) > 0:
            # Ordena pela menor f
            aberta.sort(key=lambda x: x[1])
            node, f, g, h, caminho = aberta.pop(0)

            if node == goal:
                caminho = caminho + [node]
                return (caminho, g, h)

            # Busca cidade atual na lista fechada
            if node not in [n[0] for n in fechada]:
                fechada.append((node, f, g, h))
                caminho = caminho + [node]

                # Visita todas as cidades vizinhas da cidade atual
                for vizinho in self._grafo[node]:
                    peso = self._grafo[node][vizinho][0]  # G (distância física)
                    h_aresta = self._grafo[node][vizinho][1]  # H (distância em linha reta)

                    # Busca vizinho na lista fechada e caso não esteja, recalcula F, G e H
                    if vizinho not in [n[0] for n in fechada]:
                        novo_g = g + peso
                        novo_h = h + h_aresta
                        novo_f = novo_g + novo_h

                        # Substitui se já estiver na lista aberta com f maior
                        existente = next((n for n in aberta if n[0] == vizinho), None)
                        if existente is None or novo_f < existente[1]:
                            if existente:
                                aberta.remove(existente)
                            aberta.append((vizinho, novo_f, novo_g, novo_h, caminho))

        return None
        
    def __str__(self):
        return pprint.pformat(dict(self._grafo))