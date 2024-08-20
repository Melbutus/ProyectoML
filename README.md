# Proyecto de Recomendación de Películas

Este proyecto tiene como objetivo construir un sistema de recomendación de películas utilizando datos obtenidos de un dataset de películas y créditos cinematográficos. Se aplica un proceso de ETL (Extracción, Transformación y Carga) seguido de un análisis exploratorio de datos (EDA) y la construcción de un modelo de recomendación desplegado a través de una API. Los endpoints permiten la consulta de recomendaciones, detalles de películas y estadísticas de directores y actores.

## Tabla de Contenido

- [Introducción](#introducción)
- [Instalación y Requisitos](#instalación-y-requisitos)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Uso y Ejecución](#uso-y-ejecución)
- [Datos y Fuentes](#datos-y-fuentes)
- [Metodología](#metodología)
- [Resultados y Conclusiones](#resultados-y-conclusiones)
- [Contribución y Colaboración](#contribución-y-colaboración)
- [Licencia](#licencia)

## Introducción

El objetivo de este proyecto es implementar un sistema de recomendación de películas basado en la similitud de características como calificaciones (`vote_average`, `vote_count`), géneros y descripciones de películas. El sistema está disponible a través de una API para consultas sobre recomendaciones y estadísticas de películas, directores y actores.

## Instalación y Requisitos

### Requisitos

- **Python 3.7 o superior**
- Librerías necesarias: `pandas`, `numpy`, `scikit-learn`, `fastapi`, `uvicorn`
### Instalación:

1. Clonar el repositorio:
   ```git clone https://github.com/usuario/proyecto-recomendacion-peliculas.git```

2. Crear un entorno virtual:
python    ```-m venv venv```

3. Activar el entorno virtual:
Windows: ```.\venv\Scripts\activate```
macOS/Linux: source ```venv/bin/activate```

4. Instalar las dependencias:
pip install ```-r requirements.txt```

### Estructura del Proyecto
Notebooks/: Contiene el ETL y modelo de machine learning.
Reports/: Contiene el EDA 
Datasets/: Archivos de datos procesados en formato Parquet.
src/: Código fuente del proyecto, incluyendo el código de la API.
README.md: Documentación del proyecto.

### Uso y Ejecución
Para ejecutar el ETL, EDA y el modelo de machine learning, abre los notebooks en la carpeta notebooks/.

### Para iniciar la API:
```uvicorn src.main:app --reload```

### ETL (Extracción, Transformación y Carga)
Se eliminan columnas innecesarias como original_title, homepage, adult, imdb_id, video, poster_path, tagline, status, runtime, overview del dataframe original por considerarlas como NO indispensables para el modelo y otras por ser redundantes.
Se realiza una copia del dataset original con las columnas que se creen necesarias como genres, belongs_to_collection, release_date, original_language, popularity, production_companies, production_countries, spoken_languages, id, vote_average, vote_count. A partir de ellos se extraen y limpian campos que se encuentran en listas de diccionarios/ anidados. Se combinan los datasets de películas y créditos para reducirlos y unificar la información de movies y crew. Finalmente se crean datasets específicos con la información relevante para cada función de la API.

#### Criterios Clave:
Se hizo un filtrado general para no contar con datos nulos o no disponibles.
Se limpiaron los espacios, se convirtieron los textos a minúsculas, y se verificaron los formatos.
Se transformaron los datos para que el ingreso sea independiente del uso de mayúsculas o minúsculas.
Se crearon funciones para extraer los datos de las columnas anidadas.
Los valores negativos del campo revenue fueron convertidos a positivos para no perder datos. Los valores nulos en los campos budget y revenue fueron rellenados con ceros.
Se eliminó cualquier valor nulo en la columna release_date y se creó un nuevo campo release_year a partir de release_date.

### EDA (Análisis Exploratorio de Datos)
#### objetivos:
Evaluar la cantidad y calidad de los datos disponibles.
Filtrar el dataset en función del idioma más frecuente (inglés) para optimizar el modelo.
Identificar patrones como actores y directores recurrentes en películas populares.
Examinar la distribución de valores en los campos budget, revenue, y popularity.
Generar visualizaciones que faciliten la comprensión del dataset y de los datos específicos para cada endpoint.
#### Conclusiones Relevantes:
El análisis reveló que el inglés era el idioma predominante en la mayoría de las películas, por lo que se decidió filtrar el dataset exclusivamente en este idioma, optimizando el modelo y sus resultados. Además se constató que los generos más destacados eran comedia, drama, romance. Por otro lado, había mayor cantidad de peliculas luego de los 80' pero se decidió NO filtrar por genero y año, ya que con los filtros anteriores se redujo ampliamente el numero de peliculas.

### Modelo de Recomendación
Este modelo de recomendación se basa en la similitud de características de películas y utiliza la similitud del coseno para identificar películas similares. El modelo recomienda películas basadas en características como vote_average, vote_count, y popularity.

#### Criterios del Modelo:
Dada una película de entrada, se busca su título en el dataset y se obtiene su índice.
Luego, se calculan las similitudes de coseno entre esa película y todas las demás.
Se seleccionan las n_recomendaciones más similares, excluyendo la película original.
Finalmente, se devuelven los títulos de las películas recomendadas.

### Endpoints de la API:
#### /recomendacion/{titulo}
Retorna una lista de películas recomendadas basadas en la similitud con el título dado.

#### /nombre_actor/{actor}
Proporciona estadísticas del actor, incluyendo el retorno promedio de sus películas.

#### /nombre_director/{director}
Devuelve información detallada del director, incluyendo el éxito medido por el retorno.

#### /score_titulo/{titulo}
Proporciona el puntaje promedio y el número de votaciones de la película especificada.

#### /votos_titulo/{titulo}
Retorna la cantidad de votos y el puntaje de una película si cuenta con suficiente número de valoraciones.

### Contribución y Colaboración
Las contribuciones son bienvenidas. Si deseas colaborar, puedes abrir un pull request o reportar problemas en el repositorio.

## **Fuente de datos**
- + [Dataset](https://drive.google.com/drive/folders/1X_LdCoGTHJDbD28_dJTxaD4fVuQC9Wt5?usp=drive_link): Carpeta con los 2 archivos (movies_dataset.csv y credits.csv).
+ [Diccionario de datos](https://docs.google.com/spreadsheets/d/1QkHH5er-74Bpk122tJxy_0D49pJMIwKLurByOfmxzho/edit#gid=0)
<br/>

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.
