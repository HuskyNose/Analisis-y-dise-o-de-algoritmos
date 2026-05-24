import time
from utils.graph_utils import edge_weight

class DisjointSet:
    def __init__(self, items):
        self.parent = {item: item for item in items}
        self.rank = {item: 0 for item in items}

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return False

        rank_a = self.rank[root_a]
        rank_b = self.rank[root_b]

        if rank_a < rank_b:
            self.parent[root_a] = root_b
        elif rank_a > rank_b:
            self.parent[root_b] = root_a
        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1

        return True

    def count_components(self):
        return len(set(self.find(key) for key in self.parent))

def kruskal(graph, weight_key='distance'):
    start_time = time.perf_counter()
    
    nodes = graph.get('nodes', [])
    edges = graph.get('edges', [])

    if not nodes:
        return {
            'algorithm': 'kruskal',
            'type': 'minimum_spanning_tree',
            'applicable': False,
            'message': 'El grafo está vacío.',
            'selectedEdges': [],
            'totalCost': None,
            'visitedCount': 0,
            'executionMs': (time.perf_counter() - start_time) * 1000
        }

    node_ids = [node['id'] for node in nodes]
    disjoint_set = DisjointSet(node_ids)
    
    sorted_edges = sorted(edges, key=lambda e: edge_weight(e, weight_key))
    selected_edges = []
    total_cost = 0.0

    for edge in sorted_edges:
        if disjoint_set.union(edge['sourceId'], edge['targetId']):
            selected_edges.append(edge['id'])
            total_cost += edge_weight(edge, weight_key)

    components = disjoint_set.count_components()

    message = (
        'Árbol de expansión mínima calculado con Kruskal.' 
        if components == 1 
        else f'Kruskal generó un bosque mínimo con {components} componentes.'
    )

    return {
        'algorithm': 'kruskal',
        'type': 'minimum_spanning_tree',
        'applicable': True,
        'message': message,
        'originId': None,
        'destinationId': None,
        'weightKey': weight_key,
        'selectedEdges': selected_edges,
        'pathEdges': selected_edges,
        'pathNodes': node_ids,
        'totalCost': round(total_cost, 4),
        'visitedCount': len(node_ids),
        'components': components,
        'executionMs': round((time.perf_counter() - start_time) * 1000, 4)
    }