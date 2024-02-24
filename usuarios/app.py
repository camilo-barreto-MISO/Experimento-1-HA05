from flask import  Flask,request
from celery import Celery
import redis
import os


celery_redis_conexion= os.environ.get("CELERYREDISCONEXION", 'redis://localhost:6379/0')
redis_host = os.environ.get("REDISHOST", 'localhost')

celery_app = Celery(__name__,broker=celery_redis_conexion)
redis_client = redis.StrictRedis(host=redis_host, port=6379, db=0)


app = Flask(__name__)

@app.route('/health', methods=['GET'])
def salud_servicio():
     if hay_conexion_bd():
          return 'healthy'
     return 'unhealthy'

@app.route('/base-de-datos', methods=['DELETE'])
def borrar_bd():
     
    if os.path.exists("registro.txt"):
        os.remove("registro.txt")
    return "Base de datos eliminada"

@app.route('/base-de-datos', methods=['GET'])
def obtener_bd():
    print("Directorio actual:", os.getcwd())
    if not os.path.exists("registro.txt"):
                return ""      
    try:
        with open("registro.txt", 'r') as archivo:
            contenido = archivo.read()
            return contenido
    except Exception as e:
        return f"Error al leer el archivo: {str(e)}"


        
def hay_conexion_bd():
    valor = redis_client.get("hay_conexion_bd")
    print(valor)
    return valor.decode() == 'True' if valor else True
