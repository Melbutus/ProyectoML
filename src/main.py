from fastapi import FastAPI
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import unidecode
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
import os
import tempfile  # Importa tempfile para gestionar directorios temporales

app = FastAPI()

# .\venv\Scripts\activate para activar el entorno
# uvicorn src.main:app --reload para ejecutar la api
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload

'''import os

datasets_dir = 'Datasets'
if os.path.exists(datasets_dir):
    print(f"Archivos en {datasets_dir}: {os.listdir(datasets_dir)}")
else:
    print(f"El directorio {datasets_dir} no existe")'''
    
# Carga los archivos una vez durante la inicialización de la aplicación
try:
    df_filmaciones = pd.read_parquet('Datasets/filmaciones.parquet')
    df_score = pd.read_parquet('Datasets/score_titulo.parquet')
    df_votos = pd.read_parquet('Datasets/votos_titulo.parquet')
    df_actores = pd.read_parquet('Datasets/actor_dataset.parquet')
    df_directores = pd.read_parquet('Datasets/director_dataset.parquet')
    df_peliculas = pd.read_parquet('Datasets/dataset_completo.parquet')
    features_path = pd.read_parquet('Datasets/features_matrix.parquet').values
    print("Todos los archivos .parquet se cargaron correctamente")
except Exception as e:
    print(f"Error al cargar los archivos .parquet: {e}")

    
    
### Funciones de la API

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
    # Filtrar por título
    film = df_score[df_score['title'].str.contains(titulo, case=False, na=False)]
    
    if not film.empty:
        # Manejar valores nulos para la fecha de estreno, score y popularidad
        year = film['release_date'].dt.year.values[0] if pd.notnull(film['release_date'].values[0]) else "Año no disponible"
        score = film['vote_average'].values[0] if pd.notnull(film['vote_average'].values[0]) else "Score no disponible"
        popularity = film['popularity'].values[0] if pd.notnull(film['popularity'].values[0]) else "Popularidad no disponible"
        
        return {"mensaje": f"La película '{titulo}' fue estrenada en el año {year} con un score de {score} y una popularidad de {popularity}"}
    else:
        return {"mensaje": "Película no encontrada"}


# 4. Votos por título
@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
    titulo_normalizado = titulo.strip().lower()
    film = df_votos[df_votos['title'].str.lower().str.strip() == titulo_normalizado]
    if not film.empty:
        vote_count = film['vote_count'].values[0]
        vote_average = film['vote_average'].values[0]
        return {"mensaje": f"La película '{titulo}' cuenta con {vote_count} valoraciones, con un promedio de {vote_average}"}
    return {"mensaje": "Película no encontrada"}

# Función de la API para obtener datos de actores
@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    try:
        # Ya no necesitas normalizar nuevamente, busca directamente en el dataset
        actor_films = df_actores[df_actores['actor_name'].str.contains(nombre_actor, case=False, na=False)]
        
        if not actor_films.empty:
            count = actor_films.shape[0]  # Cantidad de películas
            total_revenue = actor_films['revenue'].sum()
            total_budget = actor_films['budget'].sum()
            
            # Calcular el retorno total y el promedio de retorno
            retorno_total = total_revenue / total_budget if total_budget > 0 else 0
            retorno_promedio = retorno_total if count > 0 else 0
            
            return {
                "mensaje": f"El actor '{nombre_actor}' ha participado en {count} filmaciones, con un retorno total de {retorno_total:.2f} y un promedio de {retorno_promedio:.2f} por filmación."
            }
        
        return {"mensaje": "Actor no encontrado"}
    
    except Exception as e:
        return {"mensaje": f"Error interno: {str(e)}"}
    


@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):
    try:
        # Filtrar las películas dirigidas por el director
        director_films = df_directores[df_directores['director_name'].str.contains(nombre_director, case=False, na=False)].drop_duplicates(subset=['title', 'release_date'])

        if director_films.empty:
            return {"mensaje": f"Director '{nombre_director}' no encontrado."}

        # Variables para el cálculo del éxito a través del retorno
        total_return = 0
        num_peliculas_con_retorno = 0

        # Listas para almacenar películas con y sin datos completos
        peliculas_con_datos = []
        peliculas_sin_datos = []

        for _, film in director_films.iterrows():
            title = film['title']
            release_date = film['release_date'].strftime('%Y-%m-%d') if pd.notnull(film['release_date']) else "Fecha no disponible"
            budget = film['budget'] if pd.notnull(film['budget']) and film['budget'] > 0 else None
            revenue = film['revenue'] if pd.notnull(film['revenue']) and film['revenue'] > 0 else None
            
            if budget is not None and revenue is not None:
                retorno = round(revenue / budget, 2)
                total_return += retorno
                num_peliculas_con_retorno += 1
                # Guardar película con datos completos, si los datos como revenue, budget o return son none no hace el append y queda sin los datos anteriores
                peliculas_con_datos.append(f"- Título: {title}\n  Fecha de lanzamiento: {release_date}\n  Retorno: {retorno}\n  Costo: {budget}\n  Ganancia: {revenue}")
        
        # Calcular el retorno promedio
        promedio_retorno = round(total_return / num_peliculas_con_retorno, 2) if num_peliculas_con_retorno > 0 else "No disponible"

        # Construir el mensaje final
        mensaje = f"El director '{nombre_director}' ha dirigido las siguientes películas:\n"
        if peliculas_con_datos:
            mensaje += "\n**Películas con datos completos:**\n" + "\n\n".join(peliculas_con_datos) + "\n"
        if peliculas_sin_datos:
            mensaje += "\n**Películas con datos incompletos:**\n" + "\n\n".join(peliculas_sin_datos) + "\n"

        # Agregar el retorno total y promedio al mensaje
        mensaje += f"\nÉxito del director medido a través del retorno:\nRetorno total: {round(total_return, 2) if total_return > 0 else 'No disponible'}\nPromedio de retorno por filmación: {promedio_retorno}"

        return {"mensaje": mensaje}

    except Exception as e:
        return {"mensaje": f"Error interno: {str(e)}"}
    
# Usar una ruta temporal segura para escribir el archivo y evitar problemas de permisos en render
# features_path = os.path.join(tempfile.gettempdir(), 'features_matrix.parquet')
# Cargar o generar el features_matrix en memoria
def cargar_o_generar_features_matrix():
    features_path = 'Datasets/features_matrix.parquet'
    if os.path.exists(features_path):
        # Si el archivo existe, cargarlo
        print(f"Cargando features_matrix desde {features_path}")
        return pd.read_parquet(features_path).values
    else:
        # Generar features_matrix en memoria si el archivo no existe
        print(f"Archivo no encontrado, generando features_matrix en memoria.")
        df_peliculas = pd.read_parquet('Datasets/dataset_completo.parquet')
        
        # Normalizamos las columnas de interés
        features = df_peliculas[['vote_average', 'vote_count']]
        scaler = MinMaxScaler()
        features_matrix = scaler.fit_transform(features)
        
        # Guardar la matriz generada para futuras ejecuciones
        features_df = pd.DataFrame(features_matrix, columns=['vote_average', 'vote_count'])
        features_df.to_parquet(features_path)
        
        return features_matrix

# Cargar o generar la matriz de características
features_matrix = cargar_o_generar_features_matrix()

# Cargar el dataset de películas
@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str, n_recomendaciones: int = 5):
    # Normalizamos el título para la búsqueda
    titulo = titulo.lower().strip()

    # Verificamos si el título existe en el dataset
    if titulo not in df_peliculas['title'].str.lower().values:
        return {"mensaje": f"El título '{titulo}' no se encuentra en el dataset."}
    
    # Obtener el índice de la película
    idx = df_peliculas[df_peliculas['title'].str.lower() == titulo].index[0]
    
    # Calcular las similitudes utilizando la matriz de características
    cosine_similarities = cosine_similarity([features_matrix[idx]], features_matrix).flatten()
    
    # Obtener los índices de las películas más similares (excluyendo la película original)
    similar_indices = cosine_similarities.argsort()[::-1][1:]
    recomendaciones = []
    
    # Agregar las películas recomendadas
    for index in similar_indices:
        pelicula = df_peliculas.iloc[index]['title']
        if pelicula not in recomendaciones:
            recomendaciones.append(pelicula)
        if len(recomendaciones) >= n_recomendaciones:
            break
    
    return {"recomendaciones": recomendaciones}





