import os
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

async def custom_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        status_code = exc.status_code
        message = exc.detail
    else:
        status_code = getattr(exc, "status_code", 500)
        message = getattr(exc, "message", str(exc))

    payload = {
        "ok": False,
        "message": "Error interno del servidor." if status_code == 500 else message
    }

    if hasattr(exc, "details"):
        payload["details"] = exc.details

    if os.getenv("NODE_ENV") != "production" and status_code == 500:
        payload["debug"] = str(exc)

    return JSONResponse(status_code=status_code, content=payload)