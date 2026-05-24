from models import history_model

def list_history(limit: int = 20):
    return history_model.list_runs(limit)

def clear_history():
    return history_model.clear_runs()
