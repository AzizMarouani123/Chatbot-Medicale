import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
import pickle

# Charger le dataset
def load_data(csv_file):
    df = pd.read_csv(csv_file)

    # Nettoyage basique
    df.dropna(inplace=True)  # Supprimer les valeurs manquantes
    df.drop_duplicates(inplace=True)  # Supprimer les doublons
    df.reset_index(drop=True, inplace=True)
    
    return df

# Convertir les questions en embeddings avec Sentence-BERT
def generate_embeddings(df):
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Modèle BERT léger et efficace
    embeddings = model.encode(df['question'].tolist(), convert_to_tensor=True)

    # Sauvegarder les embeddings et le modèle
    with open("embeddings.pkl", "wb") as f:
        pickle.dump(embeddings, f)
    
    return embeddings

# Exécuter le traitement
if __name__ == "__main__":
    df = load_data("medquad.csv")
    embeddings = generate_embeddings(df)

    # Sauvegarder le dataset nettoyé
    df.to_csv("cleaned_medquad.csv", index=False)
