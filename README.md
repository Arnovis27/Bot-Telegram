# Bot-Telegram
Programa usado para potencializar el consumo de una API, en este caso se uso POKEAPI para identificar los datos de los pokemon tales como su tipo, naturaleza, estadisticas bases, entre otras cosas

## Instalación
Puedes intalarlo clonando el repositorio
```git clone url```

## Como se usa
desde la consola de comandos CMD debes ejecutar el archivo [Bot2.0.py](./Bot2.0.py) para iniciar el programa

### Conexion
Se solicita la creacion del agente virtual de telegram para generar el token de validacion, luego se consume generar las entradas de cada parametro para investigar su realizacion, continuamente se evalua el funcionamiento, acontinuacion se obtiene la url donde vamos a obtener los datos [https://pokeapi.co/](https://pokeapi.co/)

### Proceso
Mediante una peticion GET se llama a una URL que lleva como parametro la nombre del pokemon, como el formato que nos da en respuesta es un JSON, para acceder a cada parametro necesitamos acceder a cada posicion de la matriz y diccionarios, segun la informacion que necesitemos.

### Servidor
Heroku es una plataforma que nos montar en un servidor por cierto limite de forma gratuita mensualmente, para subirlo necesitamos crear un archivo con pip freeze > requirements.txt , el cual es usado para que heroku instale las librerias usadas al momento de montar el proyecto, del mismo modo creamos un archivo llamado Procfile que es un mecanismo para declarar qué comandos ejecuta su aplicación en la plataforma Heroku
