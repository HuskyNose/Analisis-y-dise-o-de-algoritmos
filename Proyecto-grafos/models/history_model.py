import json
import sqlite3
import math
from config.config import db

def _get_finite_number(val):
    if val is None:
        return None
    try:
        num = float(val)
        return num if math.isfinite(num) else None
    except (ValueError, TypeError):
        return None

def create_run(run):
    cursor = db.cursor()
    
    sql = '''
        INSERT INTO algorithm_runs (
            algorithm, origin_id, destination_id, weight_key, total_cost,
            visited_count, execution_ms, result_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''
    
    result_data = run.get('result', run)
    result_json = json.dumps(result_data)
    
    params = (
        run.get('algorithm'),
        run.get('originId'),
        run.get('destinationId'),
        run.get('weightKey', 'distance'),
        _get_finite_number(run.get('totalCost')),
        _get_finite_number(run.get('visitedCount')),
        _get_finite_number(run.get('executionMs')),
        result_json
    )
    
    cursor.execute(sql, params)
    db.commit()
    
    return {**run, 'id': cursor.lastrowid}

def list_runs(limit=20):
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    
    sql = '''
        SELECT * FROM algorithm_runs
        ORDER BY datetime(created_at) DESC
        LIMIT ?
    '''
    
    cursor.execute(sql, (limit,))
    rows = cursor.fetchall()
    
    return [{
        'id': row['id'],
        'algorithm': row['algorithm'],
        'originId': row['origin_id'],
        'destinationId': row['destination_id'],
        'weightKey': row['weight_key'],
        'totalCost': float(row['total_cost']) if row['total_cost'] is not None else None,
        'visitedCount': row['visited_count'],
        'executionMs': float(row['execution_ms']) if row['execution_ms'] is not None else None,
        'result': json.loads(row['result_json']) if row['result_json'] else None,
        'createdAt': row['created_at']
    } for row in rows]

def clear_runs():
    cursor = db.cursor()
    cursor.execute('DELETE FROM algorithm_runs')
    db.commit()
    return True