# Proyecto de Recomendación de Películas

Este proyecto inicial tiene como objetivo desarrollar un sistema de recomendación de películas para una start-up de agregación de plataformas de streaming. El sistema aprovecha un modelo de Machine Learning para recomendar películas basadas en similitudes de características como calificaciones y popularidad. Se desplegó una API que permite realizar consultas sobre recomendaciones y obtener estadísticas de películas, directores y actores.


![image](https://github.com/user-attachments/assets/31ae1710-f946-41f4-8c5e-6a7418cfeb88)

## Tabla de Contenido
- [Contexto](Contexto)
- [Instalación](#instalación)
- [Proceso de trabajo](#Proceso-de-trabajo)
- [Datos y Fuentes](#datos-y-fuentes)
  
## Contexto
El rol consistió en hacer el labor de un **Data Scientist**, diseñando y desplegando este sistema de recomendación desde cero. Partimos de datos desorganizados y sin procesar, por lo que también se ha implementado un proceso de ETL (Extracción, Transformación y Carga) para limpiar y estructurar los datos. 

## Instalación 
- Librerías necesarias: `pandas`, `numpy`, `scikit-learn`, `fastapi`, `uvicorn`

1. Clonar el repositorio:
   ```git clone https://github.com/usuario/proyecto-recomendacion-peliculas.git```

2. Crear un entorno virtual:
python    ```-m venv venv```

3. Activar el entorno virtual:
Windows: ```.\venv\Scripts\activate```
macOS/Linux: source ```venv/bin/activate```

4. Instalar las dependencias:
pip install ```-r requirements.txt```

## Proceso de trabajo
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

## **Fuente de datos**
- + [Dataset](https://drive.google.com/drive/folders/1X_LdCoGTHJDbD28_dJTxaD4fVuQC9Wt5?usp=drive_link): Carpeta con los 2 archivos (movies_dataset.csv y credits.csv).
+ [Diccionario de datos](https://docs.google.com/spreadsheets/d/1QkHH5er-74Bpk122tJxy_0D49pJMIwKLurByOfmxzho/edit#gid=0)
<br/>
