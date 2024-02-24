import requests
import time
from datetime import datetime, timezone,timedelta
from celery import Celery
import os

celery_redis_conexion= os.environ.get("CELERYREDISCONEXION", 'redis://localhost:6379/0')
url_salud_usuarios =  os.environ.get("URLSALUDUSUARIOS","http://localhost:5000/health")


celery_app = Celery(__name__,broker=celery_redis_conexion)

estado_actual = "healthy"

@celery_app.task(name='reencolar_tareas_pendientes')
def reprocesar_tareas_pendientes():
    pass



def llamar_api():
    global estado_actual
    try:
        # Realizar la llamada a la API
        respuesta = requests.get(url_salud_usuarios)

        # Verificar el estado de la respuesta
        if respuesta.status_code == 200:
            estado_salud_recuperado = respuesta.text
            print(f"{datetime.now(timezone.utc) - timedelta(hours=5)} salud servicio usuarios: {estado_salud_recuperado}.")
            
            if estado_salud_recuperado != estado_actual:
                if estado_salud_recuperado == "healthy":
                    reprocesar_tareas_pendientes.apply_async(queue = 'registo_usuario_pendientes')
                    print('Se  envía el comando para realizar tareas de compensación')

                estado_actual = estado_salud_recuperado
                print(f'estado actual {estado_actual}')
                    
        else:
            print(f"Error en la llamada a la API. Código de estado: {respuesta.status_code}")
    
    except Exception as e:
        print(f"Error: {e}")

# Intervalo en segundos entre llamadas a la API
intervalo_segundos = 5  

while True:
    llamar_api()
    time.sleep(intervalo_segundos)