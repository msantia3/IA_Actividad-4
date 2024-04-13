import numpy as np
import sys
from sklearn.cluster import KMeans

class Graph:
    def __init__(self, vertices, labels):
        self.V = vertices
        self.labels = labels
        self.graph = [[(0, 0, 0) for column in range(vertices)]
                      for row in range(vertices)]
        self.parent = [-1] * vertices  # Para trazar la ruta
    
    def add_edge(self, u, v, distance, time, cost):
        self.graph[u][v] = (distance, time, cost)
        self.graph[v][u] = (distance, time, cost)

    def print_solution(self, dist, src, target):
        # Rastreamos la ruta desde el destino al origen
        path = []
        step = target
        while step != -1:
            path.append(step)
            step = self.parent[step]
        path.reverse()  # Revertimos para mostrar de origen a destino
        
        # Imprimir la ruta
        route = " -> ".join(self.labels[p] for p in path)
        print(f"Mejor ruta desde {self.labels[src]} hasta {self.labels[target]} seleccionada por el grupo:")
        print(route)
        print(f"Distancia total: {dist[target][0]} km")
        print(f"Tiempo total: {dist[target][1]} minutos")
        print(f"Costo total: ${dist[target][2]}")

    def dijkstra(self, src, target):
        dist = [(sys.maxsize, sys.maxsize, sys.maxsize)] * self.V
        dist[src] = (0, 0, 0)
        spt_set = [False] * self.V

        for cout in range(self.V):
            u = self.min_distance(dist, spt_set)
            spt_set[u] = True

            for v in range(self.V):
                if (self.graph[u][v][0] > 0 and not spt_set[v] and
                        dist[v][2] > dist[u][2] + self.graph[u][v][2]):
                    dist[v] = (dist[u][0] + self.graph[u][v][0], dist[u][1] + self.graph[u][v][1],
                               dist[u][2] + self.graph[u][v][2])
                    self.parent[v] = u  # Guardamos el padre para trazar la ruta

        self.print_solution(dist, src, target)

    def min_distance(self, dist, spt_set):
        min = sys.maxsize
        min_index = -1
        for v in range(self.V):
            if dist[v][2] < min and not spt_set[v]:
                min = dist[v][2]
                min_index = v
        return min_index

def get_valid_input(prompt, labels):
    while True:
        value = input(prompt).strip().upper()
        if value in labels:
            return labels.index(value)
        else:
            print(f"Entrada inválida. Por favor, elija entre {', '.join(labels)}.")

def apply_kmeans(data):
    kmeans = KMeans(n_clusters=2, random_state=0).fit(data)
    return kmeans.labels_

# Crear el grafo con 5 vértices (A, B, C, D, E)
labels = ['A', 'B', 'C', 'D', 'E']
g = Graph(5, labels)
g.add_edge(0, 1, 5, 10, 7)    # A-B
g.add_edge(0, 2, 3, 5, 4)     # A-C
g.add_edge(1, 3, 7, 15, 11)   # B-D
g.add_edge(1, 4, 8, 20, 10)   # B-E
g.add_edge(2, 4, 2, 10, 2)    # C-E
g.add_edge(3, 4, 1, 5, 1)     # D-E

# Datos para K-Means (distancia, tiempo, costo)
data = np.array([[5, 10, 7], [3, 5, 4], [7, 15, 11], [8, 20, 10], [2, 10, 2], [1, 5, 1]])
clusters = apply_kmeans(data)

# Ejecutar Dijkstra en el grupo deseado
src = get_valid_input("Ingrese el punto de partida (A, B, C, D, E): ", labels)
dest = get_valid_input("Ingrese el punto de destino (A, B, C, D, E): ", labels)

g.dijkstra(src, dest)
