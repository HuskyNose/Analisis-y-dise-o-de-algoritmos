from fastapi import APIRouter, HTTPException, Query
from services import history_service

router = APIRouter()

@router.get("/")
def list_history(limit: int = Query(20)):
    try:
        limit = min(limit, 100)
        data = history_service.list_history(limit)
        return {"ok": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/")
def clear_history():
    try:
        history_service.clear_history()
        return {"ok": True, "message": "Historial eliminado."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))