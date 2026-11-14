# Pipeline ETL y EDA: Asteroides Cercanos a la Tierra (NASA NeoWs API)

Proyecto de integración de datos que implementa un flujo de Ciencia de Datos: extracción paginada desde una API REST pública, almacenamiento de documentos crudos en MongoDB y Análisis Exploratorio de Datos (EDA) en Python.

## Objetivo
Consumir la API *Near Earth Object Web Service (NeoWs)* de la NASA para extraer registros de asteroides cercanos a la Tierra, almacenarlos sin alteraciones (RAW) en una base de datos NoSQL local (`MongoDB`) y realizar limpieza, cálculo de métricas estadísticas y visualizaciones en Jupyter Notebook.

## Tecnologías y Dependencias
* **Lenguaje:** Python 3.10+
* **Base de Datos:** MongoDB Community Server (Local)
* **Librerías:** `requests`, `pymongo`, `pandas`, `matplotlib`, `seaborn`, `numpy`, `jupyter`

## Estructura del Repositorio
* `ingesta.py`: Script de extracción paginada desde la API de la NASA e inserción idempotente en MongoDB (`taller3_db.raw_data`).
* `analisis.ipynb`: Jupyter Notebook con la extracción desde MongoDB, aplanamiento de estructuras JSON, auditoría de calidad de datos, cálculo de 5 insights numéricos y tablero visual de 3 gráficas.
* `requirements.txt`: Lista de dependencias del proyecto.
* `.gitignore`: Exclusión de entornos virtuales (`.venv/`), cachés de Python y puntos de control de Jupyter.
* `documentacion.md`: Bitácora técnica detallada con la arquitectura, decisiones de diseño y resolución de incidencias.

## Instrucciones de Ejecución
1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Jibyte/nasa-api-mongodb-eda
   cd nasa-api-mongodb-eda
   ```
2. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```
3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configurar la API Key:**
   * Obtener una clave gratuita en [api.nasa.gov](https://api.nasa.gov/) y asignarla a la variable `API_KEY` dentro de `ingesta.py`.
5. **Ejecutar la ingesta de datos:**
   * Asegurarse de tener el servicio de MongoDB activo en `mongodb://localhost:27017/`.
   * Ejecutar `python ingesta.py` para poblar la colección `taller3_db.raw_data`.
6. **Ejecutar el análisis exploratorio:**
   * Abrir `analisis.ipynb` en VS Code o Jupyter, seleccionar el kernel `.venv` y ejecutar todas las celdas.
