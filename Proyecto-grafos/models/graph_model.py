import sqlite3
from config.config import db

def map_node(row):
    return {
        'id': row['id'],
        'name': row['name'],
        'lat': float(row['lat']),
        'lng': float(row['lng']),
        'type': row['type'],
        'description': row['description'] or ''
    }

def map_edge(row):
    return {
        'id': row['id'],
        'sourceId': row['source_id'],
        'targetId': row['target_id'],
        'distance': float(row['distance']),
        'time': float(row['time']),
        'cost': float(row['cost']),
        'bidirectional': int(row['bidirectional']),
        'label': row['label'] or ''
    }

def get_nodes():
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute('SELECT * FROM nodes ORDER BY id ASC')
    return [map_node(row) for row in cursor.fetchall()]

def get_edges():
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute('SELECT * FROM edges ORDER BY id ASC')
    return [map_edge(row) for row in cursor.fetchall()]

def get_graph():
    return {
        'nodes': get_nodes(),
        'edges': get_edges()
    }

def replace_graph(nodes, edges):
    cursor = db.cursor()
    try:
        cursor.execute('DELETE FROM edges')
        cursor.execute('DELETE FROM nodes')

        insert_node_sql = '''
            INSERT INTO nodes (id, name, lat, lng, type, description)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        nodes_data = [
            (
                str(node['id']),
                str(node.get('name') or node['id']),
                float(node['lat']),
                float(node['lng']),
                str(node.get('type') or 'waypoint'),
                str(node.get('description') or '')
            )
            for node in nodes
        ]
        cursor.executemany(insert_node_sql, nodes_data)

        insert_edge_sql = '''
            INSERT INTO edges (id, source_id, target_id, distance, time, cost, bidirectional, label)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        edges_data = [
            (
                str(edge['id']),
                str(edge['sourceId']),
                str(edge['targetId']),
                float(edge['distance']),
                float(edge.get('time') if edge.get('time') is not None else edge['distance']),
                float(edge.get('cost') if edge.get('cost') is not None else edge['distance']),
                int(edge.get('bidirectional') if edge.get('bidirectional') is not None else 1),
                str(edge.get('label') or '')
            )
            for edge in edges
        ]
        cursor.executemany(insert_edge_sql, edges_data)

        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    return get_graph()