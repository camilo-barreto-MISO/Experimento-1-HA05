from flask import  Flask,request
from celery import Celery
import redis
import os


celery_redis_conexion= os.environ.get("CELERYREDISCONEXION", 'redis://localhost:6379/0')
redis_host = os.environ.get("REDISHOST", 'localhost')

celery_app = Celery(__name__,broker=celery_redis_conexion)
redis_client = redis.StrictRedis(host=redis_host, port=6379, db=0)

app = Flask(__name__)

@celery_app.task(name='registrar_usuario')
def registrar_usuario(*args):
    pass


@app.route('/usuario/registrar', methods=['POST'])
def registro_usuario():
        usuario=request.args.get('usuario','')
        appellido=request.args.get('apellido','')
        registrar_usuario.apply_async(args=[usuario, appellido],queue = 'registo_usuario')
        return "Inicio el proceso de registro"

@app.route('/desconectar-bd',methods=['GET'])
def desconectar_bd():
      redis_client.set("hay_conexion_bd", "False")
      return "Base de datos desconectada"

@app.route('/conectar-bd',methods=['GET'])
def conectar_bd():
      redis_client.set("hay_conexion_bd", "True")
      return "Base de datos conectada"


