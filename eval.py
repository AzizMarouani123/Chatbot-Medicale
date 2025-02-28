import random
import pandas as pd
import torch
from chatbot import find_best_answer
from sentence_transformers import util
from rouge_score import rouge_scorer

# Charger le dataset nettoyé
df = pd.read_csv("cleaned_medquad.csv")

# Sélectionner 10 questions aléatoires
sample_questions = df.sample(10)

# Initialiser ROUGE scorer
scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)

# Métriques d'évaluation
total_similarity = 0
total_rouge = 0
exact_match_count = 0

# Évaluer chaque question
for index, row in sample_questions.iterrows():
    question = row["question"]
    expected_answer = row["answer"]

    # Obtenir la réponse du chatbot
    result = find_best_answer(question)
    
    if result:
        predicted_answer = result["answer"]
        similarity_score = result["similarity_score"]

        # Calcul du score ROUGE-L
        rouge_score = scorer.score(expected_answer, predicted_answer)['rougeL'].fmeasure

        # Vérifier si la réponse est exactement la même
        exact_match = 1 if predicted_answer.strip().lower() == expected_answer.strip().lower() else 0

    else:
        predicted_answer = "Aucune réponse trouvée"
        similarity_score = 0
        rouge_score = 0
        exact_match = 0

    # Accumuler les scores
    total_similarity += similarity_score
    total_rouge += rouge_score
    exact_match_count += exact_match

    # Afficher les résultats pour chaque question
    print(f"🔹 **Question :** {question}")
    print(f"✅ **Réponse Attendue :** {expected_answer}")
    print(f"🤖 **Réponse du Chatbot :** {predicted_answer}")
    print(f"📊 **Score de Similarité :** {similarity_score:.2f}")
    print(f"📈 **Score ROUGE-L :** {rouge_score:.2f}")
    print(f"✅ **Exact Match :** {'Oui' if exact_match else 'Non'}")
    print("-" * 80)

# Moyennes des scores
average_similarity = total_similarity / 10
average_rouge = total_rouge / 10
exact_match_rate = exact_match_count / 10

# Affichage des scores globaux
print("\n🎯 **Résumé de l'évaluation** 🎯")
print(f"📊 **Moyenne Score Similarité Cosinus :** {average_similarity:.2f}")
print(f"📈 **Moyenne Score ROUGE-L :** {average_rouge:.2f}")
print(f"✅ **Taux Exact Match :** {exact_match_rate:.2%}")
