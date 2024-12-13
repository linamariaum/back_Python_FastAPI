# Back_Python_FastAPI
Backend servicio REST en Python usando FastAPI

## Instalación ambiente
Python, desde pagina oficial o en windows en consola escribir "python" e instalar desde Microsoft Store seleccionando la versión. Para verificar instalación:
> `python --version`

## Crear proyecto

1. Ubicarse en el directorio deseado
2. Instalar la extension de python en visual code (VSCode). Para ejecutar los scripts.
3. Crear un entorno virtual para el proyecto.

  > venv es para hacer el llamado a la librería de entornos virtuales

  > Comando: 'python -m venv ["Nombre_entorno_a_crear"]'

  > `python -m venv myenv`

  > El entorno virtual tendrá su propio interprete de python y las librerías que se instalen solo se instalarían para este proyecto.

  > Para activar el entorno se puede usar una de las siguientes opciones:

  >> A. En el VSCode F1 y 'selecionar interprete'. Examinar en el equipo la ruta del proyecto recién creado y al entorno, entrar a la carpeta bin y seleccionar la versión de python o la que el sistema recomiende. Se debe reiniciar la consola del IDE para reconocer y activar el entorno.
  >> B. Se puede usar el comando. Y debería ver el nombre del entorno en su terminal o simbolo del sistema.
  >>>> `source myenv/bin/activate`

4. En la consola del IDE/VSCode, instalar las dependencias, en este caso
  > `pip install fastapi uvicorn`

  > Uvicorn: Es un servidor ASGI que se utiliza para ejecutar aplicaciones FastAPI
  
5. Escribir el codigo y los servicios deseados.

## Ejecución

Comando 'uvicorn ["Nombre_archivo"]:app --reload'
> `uvicorn main:app --reload`

Se iniciará la aplicación FastAPI en el puerto por defecto (normalmente 8000) con la recarga automática activada, de modo que la aplicación se recargará automáticamente cuando realice cambios en el código.

El servicio levanta y crea un enlace de documentación interactiva
`http://127.0.0.1:8000/docs`

## Frontend
Front que consume disponible en https://github.com/linamariaum/front_Angular_appPersonas

## Enlaces
https://fastapi.tiangolo.com/es/tutorial/
