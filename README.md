# Guía Instalación y uso Backend - Netflix Recomendations

## 1. Descompimir el zip 

## 2. Acceder a la carpeta *backend-main*

## 3. Abrir una terminal en la ruta de la carpeta

## 4. Creación del entorno virtual

Para poder instalar las dependencias necesarias sin tener que hacerlo globalmente en su PC, puede crear un entorno virtual en el cual se instalarán las dependencias necesarias.

El enlace a la documentación oficial de Python es el siguiente: 
[12. Entornos virtuales y paquetes](https://docs.python.org/es/3/tutorial/venv.html)

A continuación se detallarán los pasos:

1. Ejecutar el comando de creación en la terminal abierta anteriormente.

```
python -m venv venv
```

2. Activar el entorno virtual

Si estás en Windows (Powershell) utiliza el comando:

```
. venv/Scripts/Activate.ps1
```

Si estás en Unix o MacOS utiliza el comando:

```
source venv/bin/activate
```

## 3. Instalar las dependencias

Ejecuta el comando de instalación de PIP:

```
pip install -r .\requirements.txt
```

## 5. Correr el programa

Ejecuta el comando de Flask:

```
flask run
```

## 6. Acceder al localhost

Ingresa a la siguiente url: http://127.0.0.1:5000/

En el archivo **app.py** podrás encontrar las demás rutas a visitar, dejo algunas como prueba:

[Dataset en formato JSON](http://127.0.0.1:5000/data)

[Información específica de una película](http://127.0.0.1:5000/data/Batman%20Begins)

[Algoritmo Dijkstra](http://127.0.0.1:5000/dijkstra/50%20First%20Dates/Matchday%20%20Inside%20FC%20Barcelona)

[Algoritmo Dijktra con Filtros](http://127.0.0.1:5000/dijkstra/50%20First%20Dates/Matchday%20%20Inside%20FC%20Barcelona/Series/3/4)
