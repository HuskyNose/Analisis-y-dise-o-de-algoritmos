import math
from fastapi import HTTPException
from models import graph_model

def _is_valid_number(val):
    if val is None:
        return False
    try:
        num = float(val)
        return math.isfinite(num)
    except (ValueError, TypeError):
        return False

def validate_graph_payload(nodes, edges):
    if not isinstance(nodes, list) or len(nodes) < 2:
        raise HTTPException(status_code=422, detail="El grafo debe incluir al menos dos nodos.")

    if not isinstance(edges, list) or len(edges) < 1:
        raise HTTPException(status_code=422, detail="El grafo debe incluir al menos una arista.")

    node_ids = set()
    for node in nodes:
        node_id = node.get('id')
        node_name = node.get('name')
        
        if not node_id or not node_name:
            raise HTTPException(
                status_code=422, 
                detail={"message": "Cada nodo debe incluir id y name.", "node": node}
            )
            
        node_id_str = str(node_id)
        if node_id_str in node_ids:
            raise HTTPException(status_code=422, detail=f"Nodo duplicado: {node_id_str}.")
            
        node_ids.add(node_id_str)
        
        if not _is_valid_number(node.get('lat')) or not _is_valid_number(node.get('lng')):
            raise HTTPException(status_code=422, detail=f"Coordenadas inválidas en el nodo {node_id_str}.")

    edge_ids = set()
    for edge in edges:
        edge_id = edge.get('id')
        source_id = edge.get('sourceId')
        target_id = edge.get('targetId')
        
        if not edge_id or not source_id or not target_id:
            raise HTTPException(
                status_code=422, 
                detail={"message": "Cada arista debe incluir id, sourceId y targetId.", "edge": edge}
            )
            
        edge_id_str = str(edge_id)
        if edge_id_str in edge_ids:
            raise HTTPException(status_code=422, detail=f"Arista duplicada: {edge_id_str}.")
            
        edge_ids.add(edge_id_str)
        
        if str(source_id) not in node_ids or str(target_id) not in node_ids:
            raise HTTPException(status_code=422, detail=f"La arista {edge_id_str} referencia nodos no registrados.")
            
        for key in ['distance', 'time', 'cost']:
            val = edge.get(key)
            if not _is_valid_number(val) or float(val) < 0:
                raise HTTPException(status_code=422, detail=f"Peso {key} inválido en la arista {edge_id_str}.")

def get_graph():
    return graph_model.get_graph()

def import_graph(payload):
    nodes = payload.get('nodes', [])
    edges = payload.get('edges', [])
    validate_graph_payload(nodes, edges)
    return graph_model.replace_graph(nodes, edges)