import pandas as pd
import torch
import pickle
from sentence_transformers import SentenceTransformer, util

# Charger les données et les embeddings
def load_resources():
    df = pd.read_csv("cleaned_medquad.csv")
    with open("embeddings.pkl", "rb") as f:
        embeddings = pickle.load(f)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return df, embeddings, model

df, embeddings, model = load_resources()

# Fonction pour trouver la meilleure réponse uniquement
def find_best_answer(user_question, similarity_threshold=0.5):
    """ Trouve la meilleure réponse avec ses informations associées. """
    
    # Transformer la question utilisateur en embedding
    with torch.no_grad():
        user_embedding = model.encode(user_question, convert_to_tensor=True)

    # Calculer la similarité cosinus entre la question utilisateur et les questions du dataset
    similarities = util.pytorch_cos_sim(user_embedding, embeddings).squeeze(0)

    # Trouver l'index de la meilleure correspondance
    best_idx = torch.argmax(similarities).item()
    best_score = similarities[best_idx].item()

    # Vérifier si la meilleure correspondance dépasse le seuil de similarité
    if best_score < similarity_threshold:
        return None  # Si aucune réponse n'est assez pertinente

    # Retourner la meilleure réponse avec les informations demandées
    return {
        "question": df.iloc[best_idx]["question"],
        "answer": df.iloc[best_idx]["answer"],
        "source": df.iloc[best_idx]["source"],
        "focus_area": df.iloc[best_idx]["focus_area"],
        "similarity_score": round(best_score, 2),  # Score arrondi
        "similarity_type": "Cosine Similarity"  # Type de mesure de similarité utilisée
    }
