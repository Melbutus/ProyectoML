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
#### Procesos Relevantes:
Se realiza la limpieza de columnas innecesarias como "original_title", "homepage", "adult", "imdb_id", "video", "poster_path", 'tagline' del dataframe original y luego se realiza una copia del mismo con las columnas que se creen necesarias como 'genres', 'belongs_to_collection', 'release_date', 'original_language', 'popularity', 'production_companies', 'production_countries', 'runtime', 'spoken_languages', 'id', 'vote_average', 'vote_count'. A continuación se extraen y limpian campos complejos que se encuentran en listas de diccionarios como los titulos de las peliculas, géneros, empresas de producción, países e idiomas hablados. Se combinan los datasets de películas y créditos para reducirlos y unificar la información de actores y directores. A posterior se crean datasets específicos para lo que serán los endpoints de la API.

#### Criterios Clave:
Se eliminaron duplicados para evitar múltiples registros de la misma película.
Se extrajeron los nombres de actores, directores, fechas, etc. de listas anidadas.
Dependiendo las columnas se cambiaron los nulos por 0 o simplemente se los eliminó.
Se hizo un filtrado general para no contar con datos nulos o no disponibles. Además de limpiar los espacios, convertir a minúsculas, chequear sus formatos.
Se transformaron los datos para que el ingreso sea independiente del uso de minúsculas o mayúsculas.

### EDA (Análisis Exploratorio de Datos)
#### Objetivos:
Evaluar la cantidad y calidad de los datos disponibles.
Determinar el idioma más frecuente en las películas, con el objetivo de filtrar y simplificar el dataset basado en este criterio.
Identificar patrones como los actores y directores más recurrentes en las películas, así como las palabras más comunes en los títulos.
Examinar la distribución de valores en campos clave, como el presupuesto, la recaudación, y la popularidad.
Generar visualizaciones que faciliten la comprensión del dataset y los datos específicos para cada endpoint.

#### Conclusiones Relevantes:
El análisis reveló que el inglés era el idioma predominante en la mayoría de las películas, por lo cual se decidió filtrar el dataset exclusivamente en este idioma, optimizando el modelo y sus resultados.
Se identificó una alta concentración de ciertos actores recurrentes en las películas más populares, lo cual podría influir en la representación de dichos actores en las recomendaciones.

### Modelo de Recomendación
El modelo de recomendación se fundamenta en la similitud de películas, utilizando métricas como vote_average y vote_count. A través de una matriz de características normalizadas, se calculan las similitudes entre las mismas, lo que permite recomendar las más similares a una película determinada.

#### Criterios del Modelo:
Se utiliza cosine_similarity para medir la distancia entre las películas.
Las recomendaciones se basan en los títulos más cercanos en términos de características.

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
