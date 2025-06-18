#Entorno:

El backend se encuentra desplegado en render, este sitio toma la ultima actualización del repositorio asociado al código fuente de la aplicación en este caso la rama main 
del repositorio sushi-ross.

El sitio ejecuta las instrucciones en el archivo build.sh que contiene:

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate 

comandos necesarios para iniciar el server a desplegar.
dentro de el archivo requirements.txt podemos encontrar cada uno de las librerias utilizadas en este proyecto
