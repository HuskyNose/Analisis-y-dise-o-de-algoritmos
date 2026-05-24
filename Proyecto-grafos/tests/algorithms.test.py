from algorithms.dijkstra import dijkstra
from algorithms.prim import prim
from algorithms.kruskal import kruskal

graph = {
    'nodes': [
        {'id': 'A', 'name': 'A', 'lat': 0, 'lng': 0},
        {'id': 'B', 'name': 'B', 'lat': 0, 'lng': 1},
        {'id': 'C', 'name': 'C', 'lat': 1, 'lng': 1},
        {'id': 'D', 'name': 'D', 'lat': 1, 'lng': 0}
    ],
    'edges': [
        {'id': 'AB', 'sourceId': 'A', 'targetId': 'B', 'distance': 1, 'time': 1, 'cost': 1, 'bidirectional': 1},
        {'id': 'BC', 'sourceId': 'B', 'targetId': 'C', 'distance': 2, 'time': 2, 'cost': 2, 'bidirectional': 1},
        {'id': 'CD', 'sourceId': 'C', 'targetId': 'D', 'distance': 1, 'time': 1, 'cost': 1, 'bidirectional': 1},
        {'id': 'AD', 'sourceId': 'A', 'targetId': 'D', 'distance': 5, 'time': 5, 'cost': 5, 'bidirectional': 1},
        {'id': 'AC', 'sourceId': 'A', 'targetId': 'C', 'distance': 4, 'time': 4, 'cost': 4, 'bidirectional': 1}
    ]
}

def test_dijkstra_calcula_la_ruta_minima_esperada():
    result = dijkstra(graph, 'A', 'D', 'distance')
    assert result['applicable'] is True
    assert result['pathNodes'] == ['A', 'B', 'C', 'D']
    assert result['totalCost'] == 4

def test_prim_genera_un_arbol_de_expansion_minima():
    result = prim(graph, 'A', 'distance')
    assert result['applicable'] is True
    assert len(result['selectedEdges']) == 3
    assert result['totalCost'] == 4

def test_kruskal_genera_un_arbol_de_expansion_minima():
    result = kruskal(graph, 'distance')
    assert result['applicable'] is True
    assert len(result['selectedEdges']) == 3
    assert result['totalCost'] == 4