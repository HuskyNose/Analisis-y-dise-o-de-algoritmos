import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import initialize_database

def run_init():
    try:
        print("--- PROTOCOLO DE INICIALIZACIÓN DE DATOS ---")
        initialize_database()
        print("ESTADO: Base de datos inicializada correctamente.")
        print("SISTEMA: Listo para operación en Zacatecas-UAZ.")
    except Exception as e:
        print(f"ERROR CRÍTICO: No se pudo inicializar la base de datos: {e}")

if __name__ == "__main__":
    run_init()