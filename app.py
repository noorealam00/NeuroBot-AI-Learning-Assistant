from flask import Flask, render_template, request, jsonify

import json
import pickle
import random
import numpy as np



# CREATE FLASK APPLICATION


app = Flask(__name__)



# LOAD INTENTS


with open("intents.json", "r", encoding="utf-8") as file:
    data = json.load(file)



# LOAD TRAINED ANN


with open("models/chatbot_model.pkl", "rb") as file:
    model = pickle.load(file)



# LOAD BAG OF WORDS VECTORIZER


with open("models/vectorizer.pkl", "rb") as file:
    vectorizer = pickle.load(file)


# LOAD INTENT ENCODER


with open("models/encoder.pkl", "rb") as file:
    encoder = pickle.load(file)


# CREATE RESPONSE DICTIONARY


responses = {}

for intent in data["intents"]:

    responses[intent["tag"]] = intent["responses"]



# PREDICT USER INTENT

def predict_intent(message):

    # Convert user message into Bag of Words
    vector = vectorizer.transform(
        [message.lower()]
    ).toarray()

    # Get probabilities from ANN
    probabilities = model.predict_proba(vector)[0]

    # Find highest probability
    predicted_index = np.argmax(probabilities)

    # Get confidence
    confidence = float(
        probabilities[predicted_index]
    )

    # Convert prediction number into intent name
    intent = encoder.inverse_transform(
        [predicted_index]
    )[0]

    # Show prediction in terminal for debugging
    print(
        f"Message: {message} | "
        f"Intent: {intent} | "
        f"Confidence: {confidence * 100:.2f}%"
    )

    return intent, confidence


# HOME PAGE


@app.route("/")
def home():

    return render_template("index.html")



# CHAT API

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    message = data.get(
        "message",
        ""
    ).strip()


    # Empty message
    if not message:

        return jsonify({

            "response":
                "Please type something.",

            "intent":
                "none",

            "confidence":
                0

        })


    # Predict intent
    intent, confidence = predict_intent(
        message
    )


    
    # CONFIDENCE THRESHOLD

    if confidence < 0.40:

        response = (
            "I'm not confident about what "
            "you mean. Try asking me about "
            "AI, ANN, NLP, backpropagation, "
            "activation functions, or other "
            "topics in my knowledge base."
        )


        return jsonify({

            "response":
                response,

            "intent":
                "unknown",

            "confidence":
                round(confidence * 100, 2)

        })



    # SELECT RESPONSE

    response = random.choice(
        responses[intent]
    )


    return jsonify({

        "response":
            response,

        "intent":
            intent,

        "confidence":
            round(confidence * 100, 2)

    })


# START SERVER


if __name__ == "__main__":

    print("\n================================")
    print("       NEUROBOT IS RUNNING")
    print("================================")
    print("Open your browser and visit:")
    print("http://127.0.0.1:5000")
    print("================================\n")

    app.run(debug=True)