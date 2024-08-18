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
   ```bash
   git clone https://github.com/usuario/proyecto-recomendacion-peliculas.git
Crear un entorno virtual:
python -m venv venv

Activar el entorno virtual:
Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate

Instalar las dependencias:
pip install -r requirements.txt

Estructura del Proyecto
notebooks/: Contiene el ETL, EDA y modelo de machine learning.
Datasets/: Archivos de datos procesados en formato Parquet.
src/: Código fuente del proyecto, incluyendo el código de la API.
README.md: Documentación del proyecto.

Uso y Ejecución
Para ejecutar el ETL, EDA y el modelo de machine learning, abre los notebooks en la carpeta notebooks/.

Para iniciar la API:
uvicorn src.main:app --reload

ETL (Extracción, Transformación y Carga)
Procesos Relevantes:
Se realiza la limpieza de columnas innecesarias, corrección de datos numéricos y fechas.
Se extraen y limpian campos complejos como géneros, empresas de producción, países e idiomas hablados.
Se combinan y deduplican los datasets de películas y créditos, unificando la información de actores y directores.
Se filtran películas únicamente en inglés para simplificar el modelo.

Criterios Clave:
Se eliminan duplicados para evitar múltiples registros de la misma película.
Se extraen los nombres de actores y directores de listas anidadas.
Se priorizan registros con más datos completos (presupuesto, ingresos, fecha de lanzamiento).

EDA (Análisis Exploratorio de Datos)
Objetivos:
Comprender la distribución de las películas por año, presupuesto y popularidad.
Identificar actores y directores más frecuentes en las películas.
Examinar la correlación entre las características como ingresos, presupuesto, y votaciones.

Conclusiones Relevantes:
Se identificaron patrones en el rendimiento de las películas según su presupuesto y popularidad.
Se detectó una fuerte concentración de actores recurrentes en las películas más populares.

Modelo de Recomendación
Descripción:
El modelo se basa en la similitud de películas utilizando métricas como vote_average y vote_count. Se utiliza la matriz de características normalizadas para calcular las similitudes entre películas y recomendar las más similares a una película dada.

Criterios del Modelo:

Se utiliza cosine_similarity para medir la distancia entre las películas.
Las recomendaciones se basan en los títulos más cercanos en términos de características.
Endpoints de la API
/recomendacion/{titulo}
Retorna una lista de películas recomendadas basadas en la similitud con el título dado.
/nombre_actor/{actor}
Proporciona estadísticas del actor, incluyendo el retorno promedio de sus películas.
/nombre_director/{director}
Devuelve información detallada del director, incluyendo el éxito medido por el retorno.
/score_titulo/{titulo}
Proporciona el puntaje promedio y el número de votaciones de la película especificada.
/votos_titulo/{titulo}
Retorna la cantidad de votos y el puntaje de una película si cuenta con suficiente número de valoraciones.
Contribución y Colaboración
Las contribuciones son bienvenidas. Si deseas colaborar, puedes abrir un pull request o reportar problemas en el repositorio.

Licencia
Este proyecto está bajo la Licencia MIT.

Copy code

Este README destaca los aspectos más importantes de tu proyecto, organizados de manera clara y concisa para ser utilizado en GitHub.