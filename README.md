# Movie Scrapper

Este Scrapper se ha diseñado como práctica para la asignatura de Tipología y ciclo de vida de los datos de la UOC. El objetivo del mismo es extraer metadatos de películas y otros contenidos multimedia como series o documentales. 

Estos metadatos extraídos podrán, por ejemplo, ser usados para un futuro recomendador de contenidos. Este recomendador podrá ser tanto "*content to content*", que permita recomendar a los usuarios contenidos que se adapten a sus preferencias usando datos de películas o actores, como "*content to person*" que en función de *ratings* de usuarios con gustos similares pueda recomendar películas.  

# Componentes del equipo
Esta práctica ha sido realizada por: 

- Gregorio Andrés García Menéndez
- Manuel Enrique Gómez Montero

# Scrapping
El scrapping se ha realizado en Python, usando principalmente las siguientes librerías: 

- **Requests**: Utilizado para extraer el código HTML en páginas estáticas.
- **Selenium**: Utilizado para extraer el código HTML y navegar en páginas dinámicas.
- **Beautiful Soup**: Parser utilizado para extraer información del código HTML.



# Dataset 
El dataset ha sido diseñado con una filosofía NoSQL mediante una BBDD documental, por simplicidad para la práctica se ha usado **UnQLite** ya que es una BBDD autocontenida que no requiere servidor; en un futuro podría usarse una BBDD más compleja que nos dé un mejor rendimiento y escalabilidad como puede ser MongoDB. 

El objetivo de usar una BBDD documental es, por un lado, huir de la rigidez de un modelo relacional, teniendo más flexibilidad usando json que tuplas y, por otro, tener disponibles los datos tal y como queremos consumirlos. Los agregados (o perspectivas desde las que queremos acceder a los datos) creados son: 

- **Movies**: Colección de películas. Cada película tiene propiedades generales(título, género, año...), personas que participan(actores, directores y productores), rating demográfico por edad y sexo y usuarios que han realizado *reviews* de las películas.   
- **Users**: Colección de usuarios con los ratings que han realizado de películas. 
- **Persons**: Colección de personas y las películas en las que han participado con distintos roles. 

## Ejemplos de documentos

En la carpeta html se encuentra una página web que usando Beautiful-Collapsible-JSON-Viewer muestra un ejemplo de cada documento. Dejamos una captura de cada documento: 

![Ejemplo Movie](images/json_movie.png?raw=true "Title")

![Ejemplo Person](images/json_person.png?raw=true "Title")


![Ejemplo User](images/json_user.png?raw=true "Title")

## Dataset en csv
En la carpeta "dataset/" podemos encontrar una muestra del dataset en formato csv; en este caso, al no tener la flexibilidad de una BBDD documental, nos hemos adaptado a un modelo relacional. Los ficheros disponibles, cada uno con su cabecera son: 

- **movies.csv**: Fichero que contiene información de películas.
- **persons.csv**: Fichero con información de personas que de diferente forma van a participar en las películas.
- **users.csv**: Usuarios de IMDB que han puntuado alguna película.
- **person_movie**: Fichero con relaciones entre personas y peliculas, especificando en rol que realiza en las mismas.
- **user_movie**: Fichero con relaciones entre usuarios y películas, especificando la puntuación dada por cada usuario.


La muestra que podemos encontrar en "dataset/" contiene las 100 películas de 2018 y 2019 más votadas por los usuarios. Al ser únicamente una muestra es posible que algunos ids de películas de los ficheros "user_movie.csv" y "person_movie" no se encuentren en las 100 películas extraídas del fichero "movies.csv."


# Instalación

Primero, hay que descargar el proyecto de este repositorio, bien usando la opción _Descargar_ de Github o usando git:

`git clone https://github.com/megmontero/MovieScrapper.git`


En el directorio raíz, el fichero _requirements.txt_ contiene todos los módulos de Python adicionales para que el scraper funcione. Usando pip instalará dichos módulos:

`pip install -r requirements.txt`

Uno de los módulos utilizados es selenium para poder realizar el scraping dinámico dentro de IMDB de secciones que no permiten la paginación estática.
Usamos _Google Chrome_ para realizar dicho scraping dinámico. Por lo tanto hay que configurar el scraper para que pueda encontrar la ruta del ejecutable de Google Chrome y la ruta del driver de Selenium para Chrome.

Primero descargamos el driver desde la web: https://sites.google.com/a/chromium.org/chromedriver/downloads y lo dejamos en la ruta que queramos.

Una vez instalado, hay que indicar las rutas al scraper. Para ello, modificar el fichero selenium.cfg:

## _selenium.cfg_

### Chrome executable path
Ejemplo Windows:

>> C:/Program Files (x86)/Google/Chrome/Application/chrome.exe

Ejemplo Linux: 
>> /usr/bin/google-chrome-stable

### Chrome web driver path
drivers/chromedriver.exe

Ahora, ya podemos ejecutar el scraper de la siguiente forma desde el directorio _moviescraper_:

python imdb_scraper.py

