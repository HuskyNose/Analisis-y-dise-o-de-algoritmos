import time
import heapq
from utils.graph_utils import build_adjacency, get_node_map

def prim(graph, start_id=None, weight_key='distance'):
    start_time = time.perf_counter()
    
    nodes = graph.get('nodes', [])
    edges = graph.get('edges', [])
    node_map = get_node_map(nodes)
    
    initial_node = start_id if start_id and start_id in node_map else (nodes[0]['id'] if nodes else None)
    
    if not initial_node:
        return {
            'algorithm': 'prim',
            'type': 'minimum_spanning_tree',
            'applicable': False,
            'message': 'El grafo está vacío.',
            'selectedEdges': [],
            'totalCost': None,
            'visitedCount': 0,
            'executionMs': (time.perf_counter() - start_time) * 1000
        }

    adjacency = build_adjacency(nodes, edges, weight_key)
    visited = {initial_node}
    selected_edges = []
    total_cost = 0.0
    
    pq = []
    for candidate in adjacency.get(initial_node, []):
        heapq.heappush(pq, (candidate['weight'], candidate['edgeId'], candidate['to']))

    while pq and len(visited) < len(nodes):
        weight, edge_id, to_node = heapq.heappop(pq)
        
        if to_node in visited:
            continue
            
        visited.add(to_node)
        selected_edges.append(edge_id)
        total_cost += weight
        
        for candidate in adjacency.get(to_node, []):
            if candidate['to'] not in visited:
                heapq.heappush(pq, (candidate['weight'], candidate['edgeId'], candidate['to']))

    connected = len(visited) == len(nodes)

    return {
        'algorithm': 'prim',
        'type': 'minimum_spanning_tree',
        'applicable': True,
        'message': 'Árbol de expansión mínima calculado con Prim.' if connected else 'Prim generó un árbol parcial porque el grafo tiene componentes desconectadas.',
        'originId': initial_node,
        'destinationId': None,
        'weightKey': weight_key,
        'selectedEdges': selected_edges,
        'pathEdges': selected_edges,
        'pathNodes': list(visited),
        'totalCost': round(total_cost, 4),
        'visitedCount': len(visited),
        'components': 1 if connected else 2,
        'executionMs': round((time.perf_counter() - start_time) * 1000, 4)
    }