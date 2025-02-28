import streamlit as st
import pandas as pd
from chatbot import find_best_answer
from rouge_score import rouge_scorer

# Configuration de la page
st.set_page_config(page_title="Chatbot Médical", page_icon="💬", layout="wide")

# Interface Streamlit améliorée
st.title("💬 Chatbot Médical avec BERT")
st.markdown("""
Posez une question sur un sujet médical et obtenez une réponse pertinente.
- **Modèle utilisé** : BERT (MiniLM-L6-v2)
- **Source** : Dataset Médical Kaggle
""")

# Historique des questions-réponses
if "history" not in st.session_state:
    st.session_state["history"] = []

# Barre latérale pour afficher l'historique
with st.sidebar:
    st.header("📜 Historique des Questions")
    for entry in st.session_state["history"]:
        st.write(f"➡️ {entry['question']}")
    
    if st.button("🔄 Réinitialiser l'historique"):
        st.session_state["history"] = []
        st.rerun()

# Zone de saisie utilisateur
user_question = st.text_input("🔍 Posez votre question ici :")

if user_question:
    with st.spinner("Recherche en cours... 🔎"):
        result = find_best_answer(user_question)

    # Vérifier si une réponse a été trouvée
    if result:
        st.success("✅ Réponse trouvée !")

        st.subheader("📌 Réponse")
        st.write(result['answer'])
        
        st.subheader("📚 Source")
        st.write(f"**{result['source']}** - {result['focus_area']}")

        st.subheader("📊 Score de Similarité")
        st.write(f"Score : {result['similarity_score']} | Type : {result['similarity_type']}")

    else:
        st.error("⚠️ Désolé, aucune réponse pertinente trouvée. Essayez de reformuler votre question.")

    # Ajouter à l'historique
    st.session_state["history"].append({"question": user_question, "answer": result["answer"] if result else "Aucune réponse trouvée."})

# 🔹 **Ajout du bouton d'évaluation**
st.markdown("---")  # Séparation visuelle
st.subheader("📈 Évaluation du Chatbot")

if st.button("Lancer l'évaluation 🚀"):
    with st.spinner("Évaluation en cours..."):
        # Charger le dataset
        df = pd.read_csv("cleaned_medquad.csv").sample(10)  # Sélection de 10 exemples aléatoires
        scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)

        results = []
        total_similarity = 0
        total_rouge = 0
        exact_match_count = 0

        for _, row in df.iterrows():
            question, expected_answer = row["question"], row["answer"]
            result = find_best_answer(question)

            if result:
                predicted_answer = result["answer"]
                similarity_score = result["similarity_score"]
                rouge_score = scorer.score(expected_answer, predicted_answer)['rougeL'].fmeasure
                exact_match = 1 if predicted_answer.strip().lower() == expected_answer.strip().lower() else 0
            else:
                predicted_answer, similarity_score, rouge_score, exact_match = "Aucune réponse trouvée", 0, 0, 0

            results.append({
                "Question": question,
                "Réponse Attendue": expected_answer,
                "Réponse Chatbot": predicted_answer,
                "Score Similarité": round(similarity_score, 2),
                "Score ROUGE-L": round(rouge_score, 2),
                "Exact Match": "Oui" if exact_match else "Non"
            })

            total_similarity += similarity_score
            total_rouge += rouge_score
            exact_match_count += exact_match

        # Calcul des moyennes
        avg_similarity = total_similarity / 10
        avg_rouge = total_rouge / 10
        exact_match_rate = exact_match_count / 10

        # Affichage des résultats
        st.success("✅ Évaluation terminée !")
        st.write("### 📊 Résultats détaillés")
        st.dataframe(pd.DataFrame(results))

        st.write("### 🎯 Résumé de l'évaluation")
        st.metric("📊 Moyenne Score Similarité", f"{avg_similarity:.2f}")
        st.metric("📈 Moyenne Score ROUGE-L", f"{avg_rouge:.2f}")
        st.metric("✅ Taux Exact Match", f"{exact_match_rate:.2%}")
