from fastapi import FastAPI
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import unidecode
from sklearn.preprocessing import MinMaxScaler
import os
import warnings

warnings.filterwarnings("ignore")

app = FastAPI()

# .\venv\Scripts\activate para activar el entorno
# uvicorn src.main:app --reload para ejecutar la api
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Cargar datasets preprocesados al inicializar la aplicación
try:
    df_filmaciones = pd.read_parquet('Datasets/filmaciones.parquet')
    df_score = pd.read_parquet('Datasets/score_titulo.parquet')
    df_votos = pd.read_parquet('Datasets/votos_titulo.parquet')
    df_actores = pd.read_parquet('Datasets/actor_dataset.parquet')
    df_directores = pd.read_parquet('Datasets/director_dataset.parquet')
    df_peliculas = pd.read_parquet('Datasets/dataset_completo.parquet')
    features_matrix = pd.read_parquet('Datasets/features_matrix.parquet').values
    print("Todos los archivos .parquet se cargaron correctamente")
except Exception as e:
    print(f"Error al cargar los archivos .parquet: {e}")

# Raíz de la API
'''@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de recomendaciones de películas."}'''

# 1. Cantidad de filmaciones por mes
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    meses = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
             'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12}
    mes_num = meses.get(mes.lower())
    if mes_num:
        count = df_filmaciones[df_filmaciones['release_date'].dt.month == mes_num].shape[0]
        return {"mensaje": f"{count} películas fueron estrenadas en el mes de {mes.capitalize()}"}
    return {"mensaje": f"Mes '{mes}' no es válido."}

# 2. Cantidad de filmaciones por día
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    dias = {'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3, 'viernes': 4, 'sábado': 5, 'domingo': 6}
    dia_num = dias.get(dia.lower())
    if dia_num is not None:
        count = df_filmaciones[df_filmaciones['release_date'].dt.dayofweek == dia_num].shape[0]
        return {"mensaje": f"{count} películas fueron estrenadas los días {dia.capitalize()}"}
    return {"mensaje": f"Día '{dia}' no es válido."}

# 3. Score por título
@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    try:
        # Buscar la película en el dataset filtrando por título
        film = df_score[df_score['title'].str.contains(titulo, case=False, na=False)]

        # Verificar si se encontró la película
        if not film.empty:
            # Obtener el año de estreno, score (promedio de votos) y popularidad, manejando valores nulos
            year = int(film['release_date'].dt.year.values[0]) if pd.notnull(film['release_date'].values[0]) else "Año no disponible"
            score = round(film['vote_average'].values[0], 1) if pd.notnull(film['vote_average'].values[0]) else "Score no disponible"
            popularity = round(film['popularity'].values[0], 2) if pd.notnull(film['popularity'].values[0]) else "Popularidad no disponible"

            # Devolver el mensaje con el formato deseado
            return {
                "mensaje": f"La película '{titulo}' fue estrenada en el año {year} con un promedio de votos (score) de {score} y una popularidad de {popularity}."
            }
        else:
            return {"mensaje": "Película no encontrada"}

    except Exception as e:
        return {"mensaje": f"Error interno: {str(e)}"}

# 4. Votos por título
@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
    try:
        # Normalizar el título ingresado
        titulo_normalizado = titulo.strip().lower()

        # Buscar la película en el dataset
        film = df_votos[df_votos['title'].str.lower().str.strip() == titulo_normalizado]

        # Verificar si se encontró la película
        if not film.empty:
            # Obtener el año de estreno, cantidad de votos y el promedio de votaciones
            release_year = int(film['release_year'].values[0]) if 'release_year' in film.columns and pd.notnull(film['release_year'].values[0]) else "Año no disponible"
            vote_count = int(film['vote_count'].values[0]) if pd.notnull(film['vote_count'].values[0]) else 0
            vote_average = round(film['vote_average'].values[0], 1) if pd.notnull(film['vote_average'].values[0]) else 0

            # Formar el mensaje de salida
            return {
                "mensaje": f"La película '{titulo}' fue estrenada en el año {release_year}. "
                           f"La misma cuenta con un total de {vote_count} valoraciones, "
                           f"con un promedio de {vote_average}."
            }
        else:
            return {"mensaje": "Película no encontrada"}

    except Exception as e:
        return {"mensaje": f"Error interno: {str(e)}"}

# 5. Obtener datos de actores
@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    try:
        # Filtrar las películas en las que el actor ha participado
        actor_films = df_actores[df_actores['actor_name'].str.contains(nombre_actor, case=False, na=False)]

        if actor_films.empty:
            return {"mensaje": f"Actor '{nombre_actor}' no encontrado."}

        # Contar la cantidad de películas únicas
        count = actor_films['title'].nunique()  
        
        # Sumar el retorno total y calcular el promedio de retorno
        total_return = actor_films['return'].sum()  
        promedio_retorno = total_return / count if count > 0 else 0

        # Generar el mensaje de salida con el formato solicitado
        return {
            "mensaje": f"El actor '{nombre_actor}' ha participado de {count} filmaciones, "
                       f"el mismo ha conseguido un retorno de {total_return:.2f} "
                       f"con un promedio de {promedio_retorno:.2f} por filmación."
        }

    except Exception as e:
        return {"mensaje": f"Error interno: {str(e)}"}

# 6. Obtener datos de directores
@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):
    try:
        # Filtrar las películas dirigidas por el director
        director_films = df_directores[df_directores['director_name'].str.contains(nombre_director, case=False, na=False)].drop_duplicates(subset=['title', 'release_date'])

        if director_films.empty:
            return {"mensaje": f"Director '{nombre_director}' no encontrado."}

        peliculas_con_datos = []
        total_return = 0
        num_peliculas_con_retorno = 0

        # Asegurar que las columnas 'budget' y 'revenue' sean numéricas y no tengan valores nulos
        director_films['budget'] = pd.to_numeric(director_films['budget'], errors='coerce').fillna(0)
        director_films['revenue'] = pd.to_numeric(director_films['revenue'], errors='coerce').fillna(0)

        # Recorrer cada película del director
        for _, film in director_films.iterrows():
            title = film['title']
            release_date = film['release_date'].strftime('%Y-%m-%d') if pd.notnull(film['release_date']) else "No disponible"
            budget = film['budget']
            revenue = film['revenue']

            # Calcular el retorno (incluso si el presupuesto o la ganancia son 0)
            if budget > 0:
                retorno = round(revenue / budget, 2)
            else:
                retorno = 0  # Si el presupuesto es 0, el retorno será 0
            
            total_return += retorno
            num_peliculas_con_retorno += 1

            # Guardar los datos de la película en la lista
            peliculas_con_datos.append({
                "titulo": title,
                "fecha_lanzamiento": release_date,
                "retorno": retorno,
                "costo": budget,
                "ganancia": revenue
            })

        # Calcular el retorno promedio
        promedio_retorno = round(total_return / num_peliculas_con_retorno, 2) if num_peliculas_con_retorno > 0 else 0

        # Construir el mensaje de salida
        mensaje = {
            "exito_director": {
                "retorno_total": round(total_return, 2),
                "promedio_retorno": promedio_retorno
            },
            "peliculas": peliculas_con_datos
        }

        return mensaje

    except Exception as e:
        return {"mensaje": f"Error interno: {str(e)}"}
    
# Función para normalizar el título
def limpiar_texto_completo(texto):
    if pd.isnull(texto):
        return None
    try:
        texto = str(texto).lower().strip()
        texto = ' '.join(texto.split())  # Eliminar espacios extra
        texto = unidecode.unidecode(texto)  # Eliminar caracteres especiales
    except Exception as e:
        print(f"Error procesando el texto: {texto}, Error: {e}")
        return None 
    return texto

# Cargar dataset de películas
try:
    df_peliculas = pd.read_parquet('Datasets/dataset_completo.parquet')
    print("Dataset de películas cargado correctamente.")
    
    # Verificar si la columna 'title_normalizado' existe, sino, crearla
    if 'title_normalizado' not in df_peliculas.columns:
        print("Generando columna 'title_normalizado'...")
        df_peliculas['title_normalizado'] = df_peliculas['title'].apply(limpiar_texto_completo)
    
except Exception as e:
    print(f"Error al cargar el dataset de películas: {e}")

# Endpoint de recomendación de películas
@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str, n_recomendaciones: int = 5):
    try:
        # Normalizamos el título para la búsqueda
        titulo_normalizado = limpiar_texto_completo(titulo)

        # Verificar si el título existe en el dataset
        pelicula_idx = df_peliculas[df_peliculas['title'].str.contains(titulo_normalizado, case=False, na=False)].index

        if pelicula_idx.empty:
            return {"mensaje": f"El título '{titulo}' no se encuentra en el dataset."}

        # Resetear el índice para asegurar que está alineado con la matriz de características
        df_peliculas.reset_index(drop=True, inplace=True)

        # Obtener el índice de la película en el dataset
        idx = pelicula_idx[0]

        # Asegurarse de que el índice esté dentro de los límites de la matriz de características
        if idx >= len(features_matrix):
            return {"mensaje": "Error: el índice de la película está fuera de los límites del conjunto de datos."}

        # Calcular las similitudes utilizando la matriz de características
        cosine_similarities = cosine_similarity([features_matrix[idx]], features_matrix).flatten()

        # Verificar que el número de recomendaciones sea válido
        n_recomendaciones = min(n_recomendaciones, len(cosine_similarities) - 1)

        # Obtener los índices de las películas más similares (excluyendo la película original)
        similar_indices = cosine_similarities.argsort()[::-1][1:n_recomendaciones + 1]

        # Verificar que los índices de recomendaciones están dentro del rango de filas del DataFrame
        similar_indices = [i for i in similar_indices if i < len(df_peliculas)]

        # Obtener los títulos de las películas recomendadas
        recomendaciones = df_peliculas['title'].iloc[similar_indices].tolist()

        return {"recomendaciones": recomendaciones}

    except Exception as e:
        return {"mensaje": f"Error interno en la recomendación: {str(e)}"}


