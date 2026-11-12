# Documentación del Proyecto: APIs, MongoDB y EDA

**API Seleccionada:** NASA API (https://api.nasa.gov/)

## Fase 1: Configuración del Proyecto

### Estructura de Archivos
Se creó la siguiente estructura para mantener el proyecto organizado:
- `data/`: Carpeta para archivos temporales.
- `.gitignore`: Evita subir archivos innecesarios a GitHub (como `.venv`).
- `requirements.txt`: Lista de dependencias del proyecto.
- `ingesta.py`: Script de extracción y carga a MongoDB.
- `analisis.ipynb`: Notebook para el EDA.
- `README.md`: Resumen público del proyecto.
- `documentacion.md`: Este archivo, bitácora detallada del proceso.

### Entorno Virtual y Dependencias
Para aislar las librerías del proyecto, se creó un entorno virtual (`.venv`):
1. `python -m venv .venv` (Creación)
2. `.\.venv\Scripts\activate` (Activación en Windows) / `source .venv/bin/activate` (Mac/Linux)
3. `pip install -r requirements.txt` (Instalación de librerías: `requests`, `pymongo`, `pandas`, `matplotlib`, `seaborn`, `jupyter`).

### Control de Versiones y Ramas
- Se configuró el archivo `.gitignore` para excluir el entorno virtual (`.venv/`) y archivos temporales de Python/Jupyter.
- Se adoptó una estrategia de ramas. El primer commit se realizó en la rama `chore/setup-inicial`.

### Solución de errores (Troubleshooting)
- **Error:** Fallo al instalar `pandas` ("Encountered error while generating package metadata").
- **Solución:** Se actualizaron las herramientas de empaquetado del entorno virtual ejecutando `pip install --upgrade pip setuptools wheel` antes de reinstalar.

### Conceptos Técnicos Aplicados en la Ingesta
- **Lazy Creation:** En MongoDB no es necesario usar comandos como `CREATE DATABASE`. La base de datos (`taller3_db`) y la colección (`raw_data`) se crearon automáticamente en el momento que se insertó el primer JSON.
- **Paginación de API:** La API de NeoWs devuelve lotes de 20 registros. Se implementó un bucle `while` que lee la propiedad `links.next` del JSON para saltar de página hasta alcanzar el requisito de los 100 registros.
- **Manejo de Duplicados:** Al igualar el `_id` de Mongo con el `id` de la API, se aprovechó la restricción de llave primaria de MongoDB. Un bloque `try-except` permite que el script ignore silenciosamente las colisiones, permitiendo re-ejecutar el script sin duplicar información.

### Ejecución Exitosa de Ingesta
- Se modificó `ingesta.py` para incluir logs de consola, permitiendo rastrear el progreso de paginación.
- El script se ejecutó exitosamente en el entorno virtual (`.venv`), extrayendo lotes de 20 asteroides y paginando automáticamente hasta alcanzar el objetivo.
- Se verificó en MongoDB Compass la creación de `taller3_db.raw_data` con un total de 100 documentos almacenados en formato RAW.