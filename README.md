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


# Instalación




