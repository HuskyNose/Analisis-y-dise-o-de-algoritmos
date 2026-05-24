import os
import sqlite3
from pathlib import Path

DB_PATH = os.getenv('DB_PATH', 'database/app.db')
db_file_path = Path(DB_PATH).resolve()

db_file_path.parent.mkdir(parents=True, exist_ok=True)

db = sqlite3.connect(str(db_file_path), check_same_thread=False)
db.execute('PRAGMA foreign_keys = ON')
db.execute('PRAGMA journal_mode = WAL')
db.commit()

def read_sql(file_name):
    base_dir = Path(__file__).resolve().parent.parent
    sql_path = base_dir / 'database' / file_name
    with open(sql_path, 'r', encoding='utf-8') as f:
        return f.read()

def initialize_database():
    cursor = db.cursor()
    
    cursor.executescript(read_sql('schema.sql'))
    
    cursor.execute('SELECT COUNT(*) FROM nodes')
    node_count = cursor.fetchone()[0]
    
    if node_count == 0:
        cursor.executescript(read_sql('seed.sql'))
        
    db.commit()