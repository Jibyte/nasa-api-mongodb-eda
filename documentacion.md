# Documentación Técnica: Pipeline ETL y EDA (NASA NeoWs API + MongoDB)

## 1. Arquitectura General del Proyecto
Este proyecto implementa un flujo de datos dividido en tres etapas:
1. **Extracción (Extract):** Consumo de la API REST pública *Near Earth Object Web Service (NeoWs)* de la NASA mediante peticiones HTTP (`requests`).
2. **Almacenamiento Crudo (Load - RAW):** Persistencia de los documentos JSON íntegros en una base de datos NoSQL local (`MongoDB`), garantizando idempotencia para evitar registros duplicados.
3. **Transformación y Análisis (Transform & EDA):** Lectura desde MongoDB hacia Python (`pandas`), aplanamiento de estructuras JSON anidadas, cálculo de métricas estadísticas y generación de visualizaciones (`matplotlib` / `seaborn`).

---

## 2. Fase 1: Configuración del Entorno e Infraestructura

### Estructura del Repositorio
* `ingesta.py`: Script autónomo encargado de la extracción paginada y carga en MongoDB.
* `analisis.ipynb`: Entorno interactivo (Jupyter Notebook) para la limpieza, transformación y análisis exploratorio.
* `requirements.txt`: Especificación de dependencias del proyecto.
* `.gitignore`: Reglas de exclusión para evitar el versionamiento de entornos virtuales (`.venv/`), cachés de Python (`__pycache__/`) y puntos de control de Jupyter (`.ipynb_checkpoints/`).
* `README.md`: Documentación pública orientada a la ejecución del proyecto.
* `documentation.md`: Bitácora técnica de arquitectura y decisiones de implementación.

### Aislamiento de Dependencias y Troubleshooting
* Se creó un entorno virtual aislado mediante `python -m venv .venv`.
* **Incidencia resuelta:** Al instalar `pandas==2.1.4` en Linux/Python 3.14, `pip` falló al intentar compilar metadatos desde el código fuente. Se solucionó actualizando las herramientas de empaquetado (`pip install --upgrade pip setuptools wheel`) y eliminando la restricción de versión fija de `pandas` en `requirements.txt` para permitir la descarga de un binario precompilado compatible.

---

## 3. Fase 2: Diseño e Implementación de `ingesta.py`

### Endpoint y Autenticación
Se consume el endpoint `GET https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={API_KEY}`, el cual retorna un objeto JSON paginado con una lista de objetos bajo la llave `"near_earth_objects"`.

### Mecanismo de Paginación (`while` + puntero `next`)
La API limita cada respuesta a 20 registros. Para superar el umbral mínimo de 100 registros sin hacer peticiones manuales:
* Se implementó un bucle `while asteroides_guardados < 100 and url:`.
* Al finalizar la lectura de cada lote de 20 elementos, el script extrae dinámicamente la URL de la siguiente página navegando el diccionario de respuesta: `datos.get("links", {}).get("next")`.

### Persistencia en MongoDB e Idempotencia
* **Base de datos y colección:** `taller3_db` -> `raw_data`. Se aprovecha la *Lazy Creation* de MongoDB (la estructura física se crea al insertar el primer documento).
* **Control de duplicados (Idempotencia):** Antes de ejecutar `coleccion_nasa.insert_one(asteroide)`, se sobrescribe la llave primaria interna de MongoDB asignándole el identificador único de la NASA (`asteroide['_id'] = asteroide['id']`). Si el script se ejecuta múltiples veces, MongoDB rechaza las colisiones de `_id` y un bloque `try-except` captura la excepción silenciosamente, permitiendo que el script continúe sin duplicar registros ni detenerse.

---

## 4. Fase 3: Extracción, Transformación y EDA (`analisis.ipynb`)

### Celda 1 y 2: Extracción desde MongoDB y Aplanamiento (Flattening)
Los documentos almacenados en `raw_data` contienen diccionarios anidados de múltiples niveles. Para construir una tabla bidimensional en `pandas`, se extrajeron los registros mediante `list(coleccion.find())` y se transformaron mediante un bucle iterativo:
* **Extracción segura:** Se utilizó `.get()` encadenado (`d.get('estimated_diameter', {}).get('kilometers', {}).get('estimated_diameter_max', None)`) para extraer el diámetro máximo en kilómetros sin riesgo de lanzar un `KeyError` si algún registro viniera incompleto.
* **Esquema del DataFrame resultante (`df`):**
  1. `id` (`object`): Identificador único del asteroide.
  2. `nombre` (`object`): Designación oficial de la NASA.
  3. `magnitud_absoluta` (`float64`): Brillo intrínseco del objeto (a menor valor, mayor tamaño/brillo).
  4. `diametro_km_max` (`float64`): Estimación máxima de diámetro en kilómetros.
  5. `es_peligroso` (`bool`): Clasificación oficial de asteroide potencialmente peligroso (PHA).
  6. `es_centinela` (`bool`): Indica si el objeto está bajo monitoreo continuo de impacto (*Sentry*).
* **Auditoría de calidad:** Mediante `df.info()` y `df.isnull().sum()` se verificó una muestra limpia de **300 registros** sin valores nulos en ninguna de las 6 columnas.

### Celda 3: Cálculo de Métricas Estadísticas (5 Insights)
Sobre el DataFrame limpio se aplicaron operaciones vectorizadas de `pandas`:
1. **Volumen de muestra (`len(df)`):** 300 asteroides analizados.
2. **Tendencia central de tamaño (`df['diametro_km_max'].mean()`):** Diámetro máximo promedio de `3.837 km`.
3. **Frecuencia absoluta de riesgo (`df['es_peligroso'].sum()`):** 74 asteroides catalogados como peligrosos (al sumar una serie booleana, Python evalúa `True = 1` y `False = 0`).
4. **Proporción de riesgo:** `(peligrosos / total_asteroides) * 100`, arrojando un `24.7%` de objetos peligrosos en la muestra.
5. **Valor extremo (`df.loc[df['diametro_km_max'].idxmax()]`):** `idxmax()` devuelve el índice de la fila con el valor máximo en la columna de diámetro, permitiendo recuperar el registro completo del asteroide más grande: `'1036 Ganymed (A924 UB)'` con `87.10 km`.

### Celda 3: Visualización de Datos (Dashboard Estadístico)
Se diseñó una figura compuesta (`1x3` subplots) mediante `matplotlib` con estilo editorial limpio (`#FAFAFA`), eliminación de bordes superiores/derechos (*spines*) y etiquetas directas:
1. **Gráfico de Dona (`axes[0].pie`):** Representa la proporción porcentual de `es_peligroso` (`75.3%` inofensivos frente a `24.7%` potencialmente peligrosos) con separación de segmento crítico y un indicador central del total de registros (`300`).
2. **Histograma con Línea de Referencia (`axes[1].hist`):** Analiza la distribución de frecuencias de `magnitud_absoluta` en 15 intervalos, superponiendo una línea punteada vertical (`axvline`) que señala el promedio de la muestra.
3. **Gráfico de Barras Horizontales con Degradado (`axes[2].barh`):** Filtra los 5 objetos de mayor diámetro mediante `df.nlargest(5, 'diametro_km_max')`, aplicando una escala monocromática progresiva (`plt.cm.Blues`) y anotaciones numéricas directas al extremo de cada barra.