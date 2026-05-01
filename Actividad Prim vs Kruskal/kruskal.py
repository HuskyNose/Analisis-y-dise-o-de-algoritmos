import time

class DSU:
    def __init__(self, vertices):
        self.parent = {v: v for v in range(vertices)}
        self.rank = {v: 0 for v in range(vertices)}

    def find(self, item):
        if self.parent[item] == item:
            return item
        self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, x, y):
        xroot = self.find(x)
        yroot = self.find(y)
        if xroot != yroot:
            if self.rank[xroot] < self.rank[yroot]:
                self.parent[xroot] = yroot
            elif self.rank[xroot] > self.rank[yroot]:
                self.parent[yroot] = xroot
            else:
                self.parent[yroot] = xroot
                self.rank[xroot] += 1

def kruskal(vertices, edges):
    mst_weight = 0
    # Ordenamos las aristas por peso
    edges.sort(key=lambda item: item[2])
    dsu = DSU(vertices)

    for u, v, weight in edges:
        x = dsu.find(u)
        y = dsu.find(v)
        if x != y:
            mst_weight += weight
            dsu.union(x, y)
            
    return mst_weight

if __name__ == "__main__":
    V = 5
    
    # Grafo Disperso (5 aristas)
    edges_disperso = [
        (0, 1, 10), (1, 2, 20), (2, 3, 30), (3, 4, 40), (4, 0, 50)
    ]

    # Grafo Denso (10 aristas)
    edges_denso = [
        (0, 1, 10), (1, 2, 20), (2, 3, 30), (3, 4, 40), (4, 0, 50),
        (0, 2, 15), (0, 3, 25), (1, 3, 35), (1, 4, 45), (2, 4, 5)
    ]

    print("=== RENDIMIENTO DE KRUSKAL (Promedio de 10,000 ejecuciones) ===")
    
    REPETICIONES = 10000

    # --- Ejecución Disperso ---
    start = time.perf_counter()
    for _ in range(REPETICIONES):
        # Usamos .copy() para que cada repetición tenga la lista desordenada original
        kruskal(V, edges_disperso.copy()) 
    tiempo_total_sparse = time.perf_counter() - start
    promedio_sparse = tiempo_total_sparse / REPETICIONES
    
    print(f"Grafo Disperso -> Tiempo Promedio: {promedio_sparse:.7f} seg")
    
    # --- Ejecución Denso ---
    start = time.perf_counter()
    for _ in range(REPETICIONES):
        kruskal(V, edges_denso.copy())
    tiempo_total_dense = time.perf_counter() - start
    promedio_dense = tiempo_total_dense / REPETICIONES
    
    print(f"Grafo Denso    -> Tiempo Promedio: {promedio_dense:.7f} seg")