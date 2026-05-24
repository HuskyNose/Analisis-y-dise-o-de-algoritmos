from fastapi import HTTPException, Body
from typing import List, Dict, Any, Callable

def require_fields(fields: List[str]) -> Callable:
    def validator(payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
        missing = [
            field for field in fields 
            if payload.get(field) is None or payload.get(field) == ""
        ]
        
        if missing:
            raise HTTPException(
                status_code=422, 
                detail={
                    "message": "Faltan campos obligatorios.", 
                    "missing": missing
                }
            )
            
        return payload
        
    return validator