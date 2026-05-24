from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any
from services import graph_service

router = APIRouter()

@router.get("/")
def get_graph():
    try:
        data = graph_service.get_graph()
        return {"ok": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/import")
def import_graph(payload: Dict[str, Any] = Body(...)):
    try:
        graph = graph_service.import_graph(payload)
        return {"ok": True, "message": "Grafo importado correctamente.", "data": graph}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))