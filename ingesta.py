import os
import requests
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
API_KEY = os.getenv("NASA_API_KEY")

print("1. Conectando a MongoDB...")
try:
    cliente_mongo = MongoClient("mongodb://localhost:27017/")
    db = cliente_mongo["taller3_db"]
    coleccion_nasa = db["raw_data"]
    cliente_mongo.admin.command('ping')
    print("   ¡Conexión a MongoDB exitosa!")
except Exception as e:
    print(f"   ERROR: No se pudo conectar a MongoDB. Detalle: {e}")
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
                except Exception:
                    pass
                
                if asteroides_guardados >= 100:
                    break
            
            print(f"      Total guardados hasta ahora: {asteroides_guardados}")
            url = datos.get("links", {}).get("next")
            pagina += 1
        else:
            print(f"   ERROR de la API. Código de estado: {respuesta.status_code}")
            break
            
    print(f"\n3. Proceso finalizado. Se guardaron {asteroides_guardados} asteroides nuevos.")

if __name__ == "__main__":
    extraer_y_guardar()