from celery import Celery
import redis
import json
import os


celery_redis_conexion= os.environ.get("CELERYREDISCONEXION", 'redis://localhost:6379/0')
redis_host = os.environ.get("REDISHOST", 'localhost')

celery_app = Celery(__name__,broker=celery_redis_conexion)
redis_client = redis.StrictRedis(host=redis_host, port=6379, db=0)



@celery_app.task(name='registrar_usuario',queue = 'registo_usuario')
def registrar_usuario(nombre,apellido):
    if hay_conexion_bd():
        with open('registro.txt','a') as file:
            file.write(f'se registro el usuario: {nombre} {apellido}\n')
    else:
            info_tarea = {
            'nombre': nombre,
            'apellido': apellido}
            redis_client.rpush("registros-pendientes", json.dumps(info_tarea))
            print("Se envía a la cola de registros pendientes")
    
@celery_app.task(name='reencolar_tareas_pendientes', queue = 'registo_usuario_pendientes')
def reprocesar_tareas_pendientes():
     tareas_recuperadas = redis_client.lrange("registros-pendientes", 0, -1)
     if tareas_recuperadas:
        tareas = [json.loads(tarea_json) for tarea_json in tareas_recuperadas]
        for tarea_recuperada in tareas:
            registrar_usuario.apply_async(args=(tarea_recuperada['nombre'],tarea_recuperada['apellido']))

        redis_client.delete("registros-pendientes")
          

def hay_conexion_bd():
    valor = redis_client.get("hay_conexion_bd")
    print(valor)
    return valor.decode() == 'True' if valor else True


