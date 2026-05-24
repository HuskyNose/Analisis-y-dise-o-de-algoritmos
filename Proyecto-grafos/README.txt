GEORUTAS // GRAPH-GPS

Características Principales
Motor Algorítmico: Soporte nativo para Dijkstra, Prim y Kruskal.

Criterios de Optimización: Cálculo basado en Distancia, Tiempo o Costo Ponderado.

Expansión de Red en Caliente: Permite inyectar nuevos nodos (coordenadas) y establecer enlaces (aristas) directamente desde el HUD sin reiniciar el servidor.

Base de Datos SQLite: Registro histórico de operaciones y tiempos de ejecución (ms) para análisis de complejidad algorítmica.


Requisitos Previos 
Antes de iniciar el despliegue, asegúrate de tener instalado en tu terminal:
Python 3.9+
Navegador Web Moderno (Brave, Chrome, Firefox)

Instalación y Configuración 
Sigue estos pasos tácticos para levantar el entorno de desarrollo en tu máquina local.
1. Clonar o acceder al proyecto
Abre tu terminal en la carpeta raíz del proyecto (Proyecto-grafos).

2. Crear y activar el Entorno Virtual (VENV)
Es vital para aislar las dependencias del sistema.
Windows:

python -m venv venv
.\venv\Scripts\activate

3. Instalar el arsenal de dependencias
Con el entorno activado (venv), instala los paquetes del servidor:

pip install fastapi uvicorn python-dotenv pytest
4. Inicializar la Base de Datos SQLite
Construye las tablas del historial ejecutando el script de configuración:

python database/init_db.py
Deberás ver en consola: "ESTADO: Base de datos inicializada correctamente".

 Despliegue del Servidor 
Para poner el sistema en línea, ejecuta el archivo principal desde la raíz del proyecto:

python app.py
El servidor Uvicorn se activará. Abre tu navegador web y dirígete exactamente a esta coordenada:
http://localhost:3000

 Manual 
Una vez dentro del panel de comando de GeoRutas, sigue estos pasos:

1. Cargar el Mapa Base
Dirígete a la sección DATOS TÁCTICOS (JSON) en el panel izquierdo.

Haz clic y selecciona tu archivo .json con los nodos de Zacatecas iniciales.

El mapa se centrará automáticamente y las coordenadas (selectores) se llenarán.

2. Expansión de Red (Crear tus propios nodos)
Si necesitas extender la ruta hacia la UAZ o nuevos sectores:

Ve a la sección verde EXPANSIÓN DE RED.

Paso 1: Ingresa un ID (ej. UAZ), Latitud (ej. 22.7725) y Longitud (ej. -102.5710). Presiona AÑADIR NODO.

Paso 2: Conéctalo a la red existente. Ingresa Origen (ej. D), Destino (UAZ) y un Peso (ej. 15). Presiona ESTABLECER ENLACE.

3. Ejecutar Algoritmos
Selecciona un Origen y un Destino en el bloque de Coordenadas.

Elige tu Protocolo Logístico (Criterio de peso: Distancia/Tiempo/Costo).

Selecciona el algoritmo deseado: DIJKSTRA, PRIM o KRUSKAL.

Haz clic en el botón naranja INICIAR CÁLCULO.

El resultado se trazará en el mapa central con líneas brillantes, y el panel de ANÁLISIS DE DATOS a la derecha mostrará el costo total, nodos visitados y el tiempo de ejecución real en milisegundos.