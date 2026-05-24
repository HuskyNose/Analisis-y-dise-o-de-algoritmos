import time
import heapq
from utils.graph_utils import build_adjacency, get_node_map

def dijkstra(graph, origin_id, destination_id, weight_key='distance'):
    start_time = time.perf_counter() 
    
    nodes = graph.get('nodes', [])
    edges = graph.get('edges', [])
    node_map = get_node_map(nodes)

    if origin_id not in node_map or destination_id not in node_map:
        return {
            'algorithm': 'dijkstra',
            'type': 'shortest_path',
            'applicable': False,
            'message': 'Origen o destino inexistente en el grafo.',
            'pathNodes': [],
            'pathEdges': [],
            'totalCost': None,
            'visitedCount': 0,
            'executionMs': (time.perf_counter() - start_time) * 1000 
        }

    adjacency = build_adjacency(nodes, edges, weight_key)
    distances = {node['id']: float('inf') for node in nodes}
    distances[origin_id] = 0
    
    previous_node = {}
    previous_edge = {}
    visited = set() 
    pq = [(0, origin_id)]
    
    while pq:
        current_distance, current = heapq.heappop(pq)
    
        if current_distance > distances[current]:
            continue
            
        visited.add(current)
        
        if current == destination_id:
            break
            
        for item in adjacency.get(current, []):
            neighbor = item['to']
            weight = item['weight']
            edge_id = item['edgeId']
            
            alternative = current_distance + weight
            
            if alternative < distances[neighbor]:
                distances[neighbor] = alternative
                previous_node[neighbor] = current
                previous_edge[neighbor] = edge_id
                heapq.heappush(pq, (alternative, neighbor))
                
    if distances[destination_id] == float('inf'):
        return {
            'algorithm': 'dijkstra',
            'type': 'shortest_path',
            'applicable': True,
            'message': 'No existe ruta entre el origen y el destino seleccionados.',
            'pathNodes': [],
            'pathEdges': [],
            'totalCost': None,
            'visitedCount': len(visited),
            'executionMs': (time.perf_counter() - start_time) * 1000
        }
        
    path_nodes = []
    path_edges = []
    cursor = destination_id
    
    while cursor is not None:
        path_nodes.insert(0, cursor)
        if cursor in previous_edge:
            path_edges.insert(0, previous_edge[cursor])
        cursor = previous_node.get(cursor)
        
    return {
        'algorithm': 'dijkstra',
        'type': 'shortest_path',
        'applicable': True,
        'message': 'Ruta mínima calculada correctamente.',
        'originId': origin_id,
        'destinationId': destination_id,
        'weightKey': weight_key,
        'pathNodes': path_nodes,
        'pathEdges': path_edges,
        'selectedEdges': path_edges,
        'totalCost': round(distances[destination_id], 4),
        'visitedCount': len(visited),
        'executionMs': round((time.perf_counter() - start_time) * 1000, 4)
    }