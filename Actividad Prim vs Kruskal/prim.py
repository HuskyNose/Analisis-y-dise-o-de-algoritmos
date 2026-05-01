import time
import heapq

def prim(vertices, adj_list):
    mst_weight = 0
    visited = [False] * vertices
    min_heap = [(0, 0)] 

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

def crear_lista_adyacencia(V, edges):
    """Convierte una lista de aristas en una lista de adyacencia para Prim"""
    adj_list = {i: [] for i in range(V)}
    for u, v, w in edges:
        adj_list[u].append((w, v))
        adj_list[v].append((w, u))
    return adj_list

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

    # Preparamos las estructuras (esto se hace FUERA del cronómetro)
    adj_disperso = crear_lista_adyacencia(V, edges_disperso)
    adj_denso = crear_lista_adyacencia(V, edges_denso)

    print("=== RENDIMIENTO DE PRIM (Promedio de 10,000 ejecuciones) ===")
    
    REPETICIONES = 10000

    # --- Ejecución Disperso ---
    start = time.perf_counter()
    for _ in range(REPETICIONES):
        prim(V, adj_disperso)
    tiempo_total_sparse = time.perf_counter() - start
    promedio_sparse = tiempo_total_sparse / REPETICIONES
    
    print(f"Grafo Disperso -> Tiempo Promedio: {promedio_sparse:.7f} seg")
    
    # --- Ejecución Denso ---
    start = time.perf_counter()
    for _ in range(REPETICIONES):
        prim(V, adj_denso)
    tiempo_total_dense = time.perf_counter() - start
    promedio_dense = tiempo_total_dense / REPETICIONES
    
    print(f"Grafo Denso    -> Tiempo Promedio: {promedio_dense:.7f} seg")