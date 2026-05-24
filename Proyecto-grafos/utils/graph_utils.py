import math

def normalize_weight_key(weight_key='distance'):
    allowed = ['distance', 'time', 'cost']
    return weight_key if weight_key in allowed else 'distance'

def edge_weight(edge, weight_key):
    key = normalize_weight_key(weight_key)
    try:
        val = float(edge.get(key))
        if not math.isfinite(val) or val < 0:
            raise ValueError
        return val
    except (ValueError, TypeError):
        raise ValueError(f"Peso inválido en la arista {edge.get('id')}.")

def build_adjacency(nodes, edges, weight_key='distance'):
    # Inicializamos el diccionario de adyacencia
    adjacency = {str(node['id']): [] for node in nodes}
    
    for edge in edges:
        weight = edge_weight(edge, weight_key)
        source_id = str(edge.get('sourceId'))
        target_id = str(edge.get('targetId'))
        
        if source_id not in adjacency or target_id not in adjacency:
            raise ValueError(f"La arista {edge.get('id')} referencia nodos inexistentes.")
            
        adjacency[source_id].append({
            'edgeId': edge.get('id'),
            'from': source_id,
            'to': target_id,
            'weight': weight,
            'edge': edge
        })
        
        # En Python usamos .get() por seguridad. Casteamos a entero para la comparación.
        if int(edge.get('bidirectional', 1)) == 1:
            adjacency[target_id].append({
                'edgeId': edge.get('id'),
                'from': target_id,
                'to': source_id,
                'weight': weight,
                'edge': edge
            })
            
    return adjacency

def get_edge_map(edges):
    return {str(edge['id']): edge for edge in edges}

def get_node_map(nodes):
    return {str(node['id']): node for node in nodes}