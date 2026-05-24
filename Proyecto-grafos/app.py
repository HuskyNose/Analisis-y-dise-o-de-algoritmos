import os
from pathlib import Path
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# 1. Cargar variables de entorno desde .env
load_dotenv()

# 2. Inicializar Base de Datos
from config.config import initialize_database
initialize_database()

# 3. Importar Rutas y Middlewares
from routes import index_routes, graph_routes, algorithm_routes, history_routes
from middleware.error_handler import custom_exception_handler
from middleware.not_found import not_found_handler

# 4. Inicializar la App
app = FastAPI(docs_url=None, redoc_url=None) 

# 5. Configurar Middlewares de Seguridad y CORS (Equivalente básico a Helmet)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 6. Registrar Rutas
app.include_router(index_routes.router, prefix="/api")
app.include_router(graph_routes.router, prefix="/api/graph")
app.include_router(algorithm_routes.router, prefix="/api/algorithms")
app.include_router(history_routes.router, prefix="/api/history")

# 7. Manejo de Errores Globales
app.add_exception_handler(404, not_found_handler)
app.add_exception_handler(Exception, custom_exception_handler)

# 8. Servir Archivos Estáticos y SPA (Single Page Application)
public_dir = Path(__file__).resolve().parent / "public"

# Aseguramos que la carpeta public exista para que FastAPI no lance error
public_dir.mkdir(exist_ok=True) 

# Montar carpeta estática
app.mount("/static", StaticFiles(directory=str(public_dir)), name="static")

@app.get("/{full_path:path}")
async def serve_spa(full_path: str, request: Request):
    if full_path.startswith("api/"):
        return await not_found_handler(request, Exception())
        
    file_path = public_dir / full_path
    if file_path.is_file():
        return FileResponse(file_path)
        
    return FileResponse(public_dir / "index.html")

# 9. Iniciar el Servidor
if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    env = os.getenv("NODE_ENV", "dev")
    reload = env != "production" 
    
    print(f"GeoRutas GraphGPS disponible en http://localhost:{port}")
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=reload)