import requests
from pymongo import MongoClient

API_KEY = 'M9kLQcrkMCMbFcFwhKdRp9m9BwT8MGRdgkb9mzW9'

print("1. Conectando a MongoDB...")
try:
    cliente_mongo = MongoClient("mongodb://localhost:27017/")
    db = cliente_mongo["taller3_db"]
    coleccion_nasa = db["raw_data"]
    # Hacemos una prueba rápida de conexión
    cliente_mongo.admin.command('ping')
    print("   ¡Conexión a MongoDB exitosa!")
except Exception as e:
    print(f"   ERROR: No se pudo conectar a MongoDB. ¿Está corriendo? Detalle: {e}")
    exit()

def extraer_y_guardar():
    url = f"https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={API_KEY}"
    asteroides_guardados = 0
    pagina = 1
    
    print("\n2. Iniciando extracción desde la API de la NASA...")
    
    while asteroides_guardados < 100 and url:
        print(f"   -> Pidiendo página {pagina}...")
        respuesta = requests.get(url)
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            asteroides = datos.get("near_earth_objects", [])
            print(f"      Se encontraron {len(asteroides)} asteroides en esta página.")
            
            for asteroide in asteroides:
                asteroide['_id'] = asteroide['id']
                try:
                    coleccion_nasa.insert_one(asteroide)
                    asteroides_guardados += 1
                except Exception as e:
                    # Si ya existe, no hacemos nada, pero si es otro error, lo imprimimos (opcional)
                    pass
                
                if asteroides_guardados >= 100:
                    break
            
            print(f"      Total guardados hasta ahora: {asteroides_guardados}")
            url = datos.get("links", {}).get("next")
            pagina += 1
        else:
            print(f"   ERROR de la API. Código de estado: {respuesta.status_code}")
            print(f"   Detalle del error: {respuesta.text}")
            break
            
    print(f"\n3. Proceso finalizado. Se intentaron guardar {asteroides_guardados} asteroides nuevos.")

if __name__ == "__main__":
    extraer_y_guardar()