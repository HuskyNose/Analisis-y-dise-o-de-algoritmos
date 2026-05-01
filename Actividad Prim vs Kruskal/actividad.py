import time
import heapq

# ==========================================
# 1. ESTRUCTURAS DE DATOS Y ALGORITMOS
# ==========================================

# --- KRUSKAL ---
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
    # Kruskal necesita ordenar las aristas por peso
    edges.sort(key=lambda item: item[2])
    dsu = DSU(vertices)

    for u, v, weight in edges:
        x = dsu.find(u)
        y = dsu.find(v)
        if x != y:
            mst_weight += weight
            dsu.union(x, y)
            
    return mst_weight


# --- PRIM ---
def prim(vertices, adj_list):
    mst_weight = 0
    visited = [False] * vertices
    min_heap = [(0, 0)] # Empezamos en el vértice 0 con peso 0

    while min_heap:
        weight, u = heapq.heappop(min_heap)

        if visited[u]:
            continue
            
        visited[u] = True
        mst_weight += weight

        for next_weight, v in adj_list[u]:
            if not visited[v]:
                heapq.heappush(min_heap, (next_weight, v))

    return mst_weight


# ==========================================
# 2. GRAFO ESTABLECIDO (Hardcoded)
# ==========================================
if __name__ == "__main__":
    V = 7 # Vértices del 0 al 6
    
    # Grafo definido como una lista de (origen, destino, peso)
    # Este es el formato ideal para Kruskal
    edges = [
        (0, 1, 2),
        (0, 2, 4),
        (0, 3, 7),
        (1, 3, 3),
        (1, 4, 10),
        (2, 3, 2),
        (2, 5, 5),
        (3, 4, 7),
        (3, 5, 8),
        (3, 6, 4),
        (4, 6, 6),
        (5, 6, 1)
    ]
    
    # Transformamos las aristas en una Lista de Adyacencia
    # Este es el formato ideal para Prim
    adj_list = {i: [] for i in range(V)}
    for u, v, w in edges:
        adj_list[u].append((w, v))
        adj_list[v].append((w, u)) # El grafo es no dirigido

    print("=== INICIANDO COMPARACIÓN CON GRAFO ESTÁTICO ===")
    print(f"Vértices: {V} | Aristas: {len(edges)}\n")

    # --- Ejecutar Kruskal ---
    # Pasamos una copia de las aristas (list(edges)) para que .sort() no afecte otras cosas
    start_time = time.perf_counter()
    costo_kruskal = kruskal(V, list(edges))
    tiempo_kruskal = time.perf_counter() - start_time

    # --- Ejecutar Prim ---
    start_time = time.perf_counter()
    costo_prim = prim(V, adj_list)
    tiempo_prim = time.perf_counter() - start_time

    # --- Resultados ---
    print(f"Resultado Kruskal -> Costo AEM: {costo_kruskal} | Tiempo: {tiempo_kruskal:.7f} seg")
    print(f"Resultado Prim    -> Costo AEM: {costo_prim} | Tiempo: {tiempo_prim:.7f} seg")
    
    if costo_kruskal == costo_prim:
        print("\n✅ Éxito: Ambos algoritmos encontraron el mismo costo mínimo (18).")