# app_sheet

# Sobre el código:

Este código se encarga de recopilar desde https://pokeapi.co todos los pokemones con sus stats, sus tipos y su respectiva foto.

Adicionalmente, los tipos son asociados a un dataset de legislación penal argentina, que se encarga de buscar las palabras encontradas
en los tipos de pokemon, traducirlas y verificar si esas palabras aparecen en algún artículo del Código Penal.

Posteriormente el código crea un Google Sheets que será usado para desarrollar una AppSheet de visualización y estadísticas.


# Antes de comenzar...

Para ejecutar este código en tu computadora, deberás seguir los siguientes pasos:

Luego de descargar el repositorio, deberás dirigirte a http://datos.jus.gob.ar/dataset/codificacion-de-delitos-del-codigo-penal-argentino 
y descargar el archivo en formato '.csv'

En https://console.cloud.google.com deberás crear un proyecto y habilitar las APIs de google drive y de google spreadsheets. Crea las
credenciales y posteriormente descarga el archivo '.json'

Una vez hecho esto, crea un archivo '.env' que contenga los siguientes datos:

    LAW=(el nombre con el que has guardado el archivo .csv)
    SHEETS=(el nombre con el que has guardado el archivo .json)
    PERSONAL_EMAIL=(tu correo electrónico)
    
Una vez hecho esto, solo queda que crees tu entorno virtual e instales los requerimientos con el comando:

    pip install -r .\requirements.txt
    
