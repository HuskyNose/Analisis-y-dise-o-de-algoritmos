from fastapi import Request
from fastapi.responses import JSONResponse

async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={
            "ok": False,
            "message": f"Ruta no encontrada: {request.method} {request.url.path}"
        }
    )