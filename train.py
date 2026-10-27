import json
import os
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.neural_network import MLPClassifier



# 1. LOAD THE DATASET


with open("intents.json", "r", encoding="utf-8") as file:
    data = json.load(file)


texts = []
labels = []


for intent in data["intents"]:

    for pattern in intent["patterns"]:

        texts.append(pattern.lower())

        labels.append(intent["tag"])


print("Total training examples:", len(texts))
print("Total intents:", len(set(labels)))


# 2. CONVERT TEXT INTO NUMBERS


vectorizer = CountVectorizer(
    lowercase=True,
    token_pattern=r"(?u)\b\w+\b"
)


X = vectorizer.fit_transform(texts).toarray()



# 3. CONVERT INTENT NAMES INTO NUMBERS


encoder = LabelEncoder()

y = encoder.fit_transform(labels)



# 4. CREATE THE ARTIFICIAL NEURAL NETWORK

model = MLPClassifier(

    hidden_layer_sizes=(128, 64),

    activation="relu",

    solver="adam",

    max_iter=500,

    random_state=42,

    early_stopping=True,

    validation_fraction=0.2,

    n_iter_no_change=20

)



# 5. TRAIN THE ANN


print("\nTraining ANN...")
print("Please wait...\n")


model.fit(X, y)



# 6. SHOW TRAINING INFORMATION


print("\n==============================")
print("TRAINING COMPLETE")
print("==============================")

print("Training iterations:", model.n_iter_)

print("Training accuracy:",
      round(model.score(X, y) * 100, 2), "%")


# 7. CREATE MODELS FOLDER


os.makedirs("models", exist_ok=True)



# 8. SAVE THE TRAINED ANN


with open("models/chatbot_model.pkl", "wb") as file:

    pickle.dump(model, file)



# 9. SAVE THE VECTORIZER


with open("models/vectorizer.pkl", "wb") as file:

    pickle.dump(vectorizer, file)



# 10. SAVE THE LABEL ENCODER


with open("models/encoder.pkl", "wb") as file:

    pickle.dump(encoder, file)


print("\nSaved files:")

print("✓ models/chatbot_model.pkl")

print("✓ models/vectorizer.pkl")

print("✓ models/encoder.pkl")

print("\nYour ANN is ready!")