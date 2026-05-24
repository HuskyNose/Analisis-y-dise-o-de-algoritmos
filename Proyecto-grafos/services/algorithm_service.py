from fastapi import HTTPException
from models import graph_model, history_model
from algorithms.dijkstra import dijkstra
from algorithms.prim import prim
from algorithms.kruskal import kruskal
from utils.graph_utils import normalize_weight_key

def run_algorithm(payload):
    algorithm = payload.get('algorithm')
    origin_id = payload.get('originId')
    destination_id = payload.get('destinationId')
    weight_key = payload.get('weightKey')

    graph = graph_model.get_graph()
    selected_weight_key = normalize_weight_key(weight_key)
    selected_algorithm = str(algorithm or '').lower()
    
    result = None

    if selected_algorithm == 'dijkstra':
        if not origin_id or not destination_id:
            raise HTTPException(status_code=422, detail="Dijkstra requiere origen y destino.")
        result = dijkstra(graph, origin_id, destination_id, selected_weight_key)
        
    elif selected_algorithm == 'prim':
        result = prim(graph, origin_id, selected_weight_key)
        
    elif selected_algorithm == 'kruskal':
        result = kruskal(graph, selected_weight_key)
        
    else:
        raise HTTPException(status_code=422, detail="Algoritmo no soportado. Usa dijkstra, prim o kruskal.")

    history_model.create_run({
        'algorithm': result.get('algorithm'),
        'originId': result.get('originId') or origin_id or None,
        'destinationId': result.get('destinationId') or destination_id or None,
        'weightKey': selected_weight_key,
        'totalCost': result.get('totalCost'),
        'visitedCount': result.get('visitedCount'),
        'executionMs': result.get('executionMs'),
        'result': result
    })

    return {'result': result, 'graph': graph}