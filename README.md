# 🏥 Chatbot Médical 

## 📌 Introduction

Ce projet implémente un **chatbot médical** basé sur **BERT** (*all-MiniLM-L6-v2*), capable de répondre à des questions médicales en trouvant la réponse la plus pertinente dans un dataset.  
L'application est développée en **Python** et déployée via **Docker** sur **Google Cloud Platform (GCP)**.

---

## 🛠️ 1. Prétraitement des Données (Data Processing)

Avant d'entraîner le modèle, il est crucial de **nettoyer et préparer les données** pour garantir de meilleures performances.

### 🔹 Étapes du prétraitement :
1. **Chargement du dataset** (`medquad.csv`) contenant des paires de questions-réponses médicales.
2. **Nettoyage** : suppression des valeurs manquantes et des doublons.
3. **Génération des embeddings** :
   - Utilisation de **Sentence-BERT** (`all-MiniLM-L6-v2`).
   - Conversion des questions en vecteurs numériques.
   - Sauvegarde des **embeddings** dans un fichier `embeddings.pkl` pour éviter un recalcul à chaque exécution.

💡 **Remarque** : Cette étape est exécutée **une seule fois** pour optimiser les performances.

---

## 🤖 2. Chatbot : Recherche de la Meilleure Réponse

Une fois les embeddings générés, le chatbot utilise la **similarité cosinus** pour comparer les questions posées avec celles du dataset.

### 🔹 Fonctionnement :
1. L'utilisateur pose une question via l'interface **Streamlit**.
2. Le modèle **BERT** génère un embedding pour cette question.
3. On calcule la **similarité cosinus** entre la question de l'utilisateur et celles du dataset.
4. La réponse la plus pertinente est retournée **si la similarité dépasse un seuil** (ex: `0.5`).
5. Si aucune correspondance n'est trouvée, le chatbot indique qu'il ne peut pas répondre.

### 📊 Métriques utilisées :
- **Similarité Cosinus** : mesure de la proximité entre deux phrases.
- **Score ROUGE-L** : évalue la similarité entre la réponse générée et la réponse attendue.

---

## 🎨 3. Interface Utilisateur (Streamlit)

Le chatbot est intégré à une application **Streamlit** pour une interaction fluide.

### 🔹 Fonctionnalités :
- **Posez une question** et obtenez une réponse médicale.
- **Affichage des sources** de la réponse.
- **Historique des questions** dans une barre latérale.
- **Évaluation** de la précision du chatbot sur un échantillon de questions.

---

## 📊 4. Évaluation des Performances

Une évaluation automatique est intégrée pour mesurer la qualité des réponses.

### 🔹 Méthodologie :
1. Sélection aléatoire de 10 questions du dataset.
2. Comparaison des réponses du chatbot avec les réponses réelles.
3. **Métriques analysées** :
   - Moyenne de la **similarité cosinus**.
   - Score **ROUGE-L** pour mesurer la pertinence textuelle.
   - **Taux d’exactitude** (proportion de réponses parfaitement correctes).

---

## 🏛️ 5. Création d'une Table SQL avec Cloud Final

Une table SQL est créée à l'aide du **notebook cloud_final**, permettant de stocker des documents issus d'un fichier **CSV**.

### 🔹 Objectif :
- Charger les données du fichier `medquad.csv`.
- Créer une table SQL pour stocker ces informations.
- Utiliser cette table pour **optimiser les recherches de réponses**.

---

## 💪 6. Conteneurisation avec Docker

Le projet est **conteneurisé avec Docker** pour faciliter le déploiement et garantir une exécution cohérente.

### 🔹 Avantages :
- **Isolation** : Toutes les dépendances sont incluses.
- **Portabilité** : Fonctionne de la même manière sur n'importe quel serveur.
- **Facilité de mise à jour** : Une nouvelle version peut être déployée sans affecter l'environnement.

---

## ☁️ 7. Déploiement sur Google Cloud Platform (GCP)

L’application est **hébergée sur GCP** via **Cloud Run** pour une mise à l'échelle automatique.

### 🔹 Étapes du déploiement :
1. **Construction et push de l’image Docker** vers **Google Container Registry (GCR)**.
2. **Déploiement de l’image** sur **Cloud Run**, qui alloue dynamiquement les ressources en fonction de la charge.
3. **Mise à disposition d’une URL publique** permettant aux utilisateurs d’accéder à l’application.

📌 **Lien vers l’application déployée** : [🔗 Accéder au Chatbot](https://mon-chatbot-medical.cloud)

---


## 🔗 9. Conclusion

Ce chatbot médical est un **outil interactif et intelligent**, offrant des réponses médicales basées sur des données validées.  
Le déploiement avec **Docker & GCP** assure une scalabilité et une accessibilité optimales.

