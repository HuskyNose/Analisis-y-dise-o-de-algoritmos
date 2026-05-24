from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any
from services import algorithm_service

router = APIRouter()

@router.post("/run")
def run_algorithm(payload: Dict[str, Any] = Body(...)):
    try:
        data = algorithm_service.run_algorithm(payload)
        return {"ok": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))