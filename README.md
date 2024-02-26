# Experimento-1-HA05

Para correr el experimento clone el repositorio en su equipo.

La implementación de los servicios está realizado en un docker compose.

Levante el compose:
`docker compose up`

## Ejecución del experimento:

En la raiz se encuentran tres colecciones de postman para correr las pruebas:
1. Experimento-1 EjecucionCargaDeDatos.postman_collection.json
2. Experimento-1 EjecucionVerificacionDeDatos.postman_collection.json
3. Experimento-1.postman_collection.json

### 1. Ejecutar el experimento, lo hicimos generando 100 iteraciones.
En esta colección los pasos son:
- Desconectamos la base de datos
- Hacemos lectura del estado de salud para verificar que el API responda que no está disponible
- Registramos el usuario sin tener conexión
- Conectamos la base de datos nuevamente
- Hacemos nuevamnete lectura del estado de salud para verificar que el API responda que está disponible

En postman corra la colección completa `Run collection`
Seleccione el archivo `usuarios.csv` que está en el repositorio para realizar las 100 iteraciones

Con esto estamos garantizando que los registros se realicen en primera instancia con un fallo de base de datos.

![Resultados del registro de usuarios](https://github.com/camilo-barreto-MISO/Experimento-1-HA05/assets/142316821/c2088a02-0648-4bd5-a83d-7d28588d91ad)

  
### 2. Ejecutar la validación. Se hace una iteración de los 100 usuarios que se debieron haber creado
La segunda colección realiza lo siguiente:
- Verificamos que el estado de salud de la base de datos sea correcto.
- Obtenemos uno por uno los usuarios que deberían haber quedado creado.

En postman corra la colección completa `Run collection`
Seleccione el archivo `usuarios.csv` que está en el repositorio para realizar las 100 iteraciones

![Resultados de la verificación](https://github.com/camilo-barreto-MISO/Experimento-1-HA05/assets/142316821/9f7c04e1-6512-4e5a-b210-5a72bb0d865e)


### 3. Volver a ejecutar el experimento
Si desea volver a ejecutar el experimento, le pedimos el favor que limpie la base de datos.

En la colección 3 Experimento-1, encuentra el servicio: **Borrar base de datos**

Por favor ejecute este API antes de volver a genrar
