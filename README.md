### Sistema de Recomendación de Películas
Este proyecto tiene como objetivo desarrollar un sistema de recomendación de películas utilizando técnicas de machine learning. A lo largo del proyecto, se ha trabajado con varios datasets, como dfmovies y dfcredits, que contienen información sobre películas, sus características, y el reparto involucrado. A continuación se detallan los pasos realizados hasta ahora.

## 1. Preparación del Dataset dfmovies - ETL

1.1 Limpieza de Datos
Manejo de Valores Nulos:
budget y revenue: Se reemplazaron los valores nulos por 0.
release_date: Se eliminaron las filas con valores nulos en esta columna.
runtime: Se identificaron y manejaron valores nulos, aunque algunos valores nulos pueden persistir.
Conversión de Tipos de Datos:
Las columnas budget y revenue fueron convertidas a enteros para facilitar cálculos y análisis.
Se creó la columna release_year extrayendo el año de release_date.

1.2 Estandarización y Normalización
Las columnas numéricas como budget, revenue, popularity, vote_average, vote_count, y runtime fueron preparadas para ser estandarizadas o normalizadas en futuras etapas del modelado.

1.3 Manejo de Datos Categóricos
Extracción de Datos de Campos Complejos:
belongs_to_collection: Se extrajo el nombre de la colección a partir de diccionarios y se creó una nueva columna nombre_coleccion.
genres: Se extrajeron los nombres de los géneros desde una lista de diccionarios y se creó la columna generos.
production_countries, production_companies, spoken_languages: Se extrajeron y consolidaron los nombres relevantes de estas listas de diccionarios.

Filtrado de Filas:
Se filtraron filas para excluir datos irrelevantes o no disponibles, asegurando que solo se retengan filas con información significativa.

## 2. Preparación del Dataset dfcredits

2.1 Limpieza de Datos
Extracción de Información Relevante:
cast: Se extrajeron los nombres de los actores y sus respectivos cast_id de una lista de diccionarios.
crew: Se extrajeron los nombres de los directores y sus id de una lista de diccionarios. Si no había un director, se marcó como "Sin director".

2.2 Unión de Datos
Se creó un nuevo DataFrame dfcredits_reducido que incluye:
Nombre de los actores (actor_name).
Nombre del director (director_name) y su director_id.
El movie_id para relacionar con otros datos.

2.3 Manejo de Valores Nulos
Se manejaron valores nulos en las columnas director_name y director_id, aunque algunos valores nulos en director_id persisten.

## 3. Preparación para el Modelado
. Preprocesamiento de textos
Antes de pasar al modelado de machine learning, es necesario preprocesar los textos:

Minúsculas: Convertir todo a minúsculas.
Eliminar signos de puntuación.
Eliminar números.
Eliminar palabras vacías (stopwords).
Tokenización, stemming o lematización (dependiendo de lo que prefieras).

3.1 Revisión de Datos
Verificación de Valores Nulos:
Se realizó una revisión para identificar y manejar valores nulos restantes en las columnas clave antes de iniciar el modelado.
Ingeniería de Características:
Se evaluó la posibilidad de crear nuevas características derivadas para mejorar el rendimiento del modelo de recomendación.

3.2 Planificación del Modelado
Se planificó la normalización y estandarización de las columnas relevantes.
Se consideraron estrategias para manejar datos categóricos, como one-hot encoding.

## 4. Próximos Pasos
Revisión Completa del Pipeline de Datos:

Revisar todo el proceso de limpieza y transformación de datos para asegurarse de que no haya errores antes de proceder al modelado.
Implementación del Sistema de Recomendación:

Seleccionar y entrenar modelos de machine learning.
Evaluar el rendimiento del modelo utilizando métricas apropiadas para sistemas de recomendación.
Optimización y Validación:

Realizar tuning de hiperparámetros y utilizar validación cruzada para mejorar la precisión del modelo.

Usar Aproximaciones para la Similitud
En lugar de calcular la similitud coseno exacta, puedes usar algoritmos de similitud aproximada como Annoy, FAISS, o HNSWlib. Estos algoritmos son mucho más eficientes y están diseñados para manejar grandes volúmenes de datos. dado que con otras herramientas me arrojaba errores por cuestiones de espacio

FAISS (Facebook AI Similarity Search):
FAISS es una biblioteca desarrollada por Facebook para realizar búsquedas eficientes y rápidas de similitud en vectores de alta dimensión. Puedes cargar los embeddings en FAISS y realizar búsquedas de similitud muy rápido, sin necesidad de mantener toda la matriz de similitud en memoria.