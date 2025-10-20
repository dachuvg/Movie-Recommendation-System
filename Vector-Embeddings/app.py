from fastapi import FastAPI, Query, HTTPException
from typing import List
import pandas as pd
import numpy as np
from ast import literal_eval
from langchain_community.vectorstores import FAISS
from langchain_ollama.embeddings import OllamaEmbeddings

app = FastAPI(title="Movie Recommender API")

# Global placeholders
vectorstore = None
embeddings = None
df_movies = None
df_credits = None
df = None

def load_data_and_vectorstore():
    global vectorstore, embeddings, df_movies, df_credits, df

    if vectorstore is not None:
        return  # already loaded

    # --- Load CSVs ---
    df = pd.read_pickle('./movies_final.pkl')
    # --- Initialize embeddings ---
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    # --- Load vectorstore ---
    try:
        vectorstore = FAISS.load_local(
            "movie_vectorstore",
            embeddings,
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        raise RuntimeError(f"Failed to load FAISS vectorstore: {e}")



# Routes
@app.get("/recommend")
def recommend(movie: str = Query(..., description="Movie title to find similar movies"), k: int = 5):
    try:
        load_data_and_vectorstore()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Find movie in dataset
    movie_row = df[df['title'].str.lower() == movie.lower()]
    print(movie_row)
    print(movie_row.columns)
    if movie_row.empty:
        raise HTTPException(status_code=404, detail="Movie not found in dataset")

    # Create metadata for query
    metadata = movie_row.iloc[0]['metadata']
    if not metadata:
        raise HTTPException(status_code=400, detail="Movie has no metadata to use for embedding")

    # Embed and search
    query_embedding = embeddings.embed_query(metadata)
    results = vectorstore.similarity_search_by_vector(query_embedding, k=k+1)

    results = results[1:k+1]  
    recommendations = [
        {
            "title": doc.metadata.get("title", "Unknown")
        }
        for doc in results
    ]
    
    return {"input_movie": movie, "recommendations": recommendations}


# @app.get("/health")
# def health():
#     """Check if server is running"""
#     return {"status": "ok"}


