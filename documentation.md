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

