from flask import Flask, request, jsonify
import torch
import numpy as np
import random
import firebase_admin
from firebase_admin import credentials, firestore
from model import NeuralNet
from utils import bag_of_words, stem
import json
from datetime import datetime

app = Flask(__name__)

# Initialize Firestore
cred = credentials.Certificate("serviceAccountKey.json")  # Replace with your service account key path
firebase_admin.initialize_app(cred)
db = firestore.client()

# Load intents and model
with open('intents.json', 'r') as f:
    intents = json.load(f)

# Load model
model = NeuralNet(input_size=123, hidden_size=8, output_size=31)
model.load_state_dict(torch.load("model.pth", weights_only=True))
model.eval()

# Load all_words and tags (defined in train.py)
with open("train_data.json", "r") as f:
    train_data = json.load(f)
    all_words = train_data["all_words"]
    tags = train_data["tags"]

# Tag responses from intents
def get_response(tag):
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

# Function to fetch weather data from Firestore
def get_weather_for_location(location):
    doc_ref = db.collection("weather_updates").document(location)
    doc = doc_ref.get()
    if doc.exists:
        weather_data = doc.to_dict()
        latest_forecast = weather_data.get("forecasts", [])[0]  # Get the most recent forecast
        response = (f"Weather in {location}:\n"
                    f"Temperature: {latest_forecast['temperature']}°C\n"
                    f"Condition: {latest_forecast['condition']}\n"
                    f"Humidity: {latest_forecast['humidity']}%\n"
                    f"Wind Speed: {latest_forecast['wind_speed']} km/h\n"
                    f"Precipitation: {latest_forecast['precipitation']} mm\n"
                    f"Feels Like: {latest_forecast['feels_like']}°C\n"
                    f"UV Index: {latest_forecast['uv_index']}\n"
                    f"Visibility: {latest_forecast['visibility']} km\n"
                    f"Updated at: {weather_data['last_updated']}")
    else:
        response = f"Sorry, I don't have weather data for {location} at the moment."
    return response

# Track users' states and information gathering progress
user_data_collection = {}

@app.route('/chatbot', methods=['POST'])
def chatbot_response():
    data = request.get_json()
    user_message = data["message"].lower()
    user_id = data.get("user_id", "unknown")  # Assuming user_id is sent in request

    # Check if the user is in the process of providing information
    if user_id in user_data_collection:
        user_data = user_data_collection[user_id]
        current_step = user_data.get("step", 0)

        if current_step == 0:
            # Ask for name
            user_data["name"] = user_message
            user_data["step"] += 1
            response = "Got it! Can you provide your address next?"

        elif current_step == 1:
            # Ask for address
            user_data["address"] = user_message
            user_data["step"] += 1
            response = "Thanks! Now, may I have your phone number?"

        elif current_step == 2:
            # Ask for phone number
            user_data["phone"] = user_message
            user_data["step"] += 1
            response = "Thank you! Please reply 'yes' to confirm and save your info."

        elif current_step == 3 and user_message in ["yes", "confirm"]:
            # Final confirmation, save as a new document to Firestore
            doc_ref = db.collection("app_users").document()
            doc_ref.set({
                "user_id": user_id,
                "name": user_data["name"],
                "address": user_data["address"],
                "phone": user_data["phone"],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            del user_data_collection[user_id]  # Clear user data after saving
            response = "Your information has been saved as a new entry. Thank you!"

        else:
            response = "Please reply 'yes' to confirm or type 'restart' to start over."

    elif "store my info" in user_message:
        # Start info collection process
        user_data_collection[user_id] = {"step": 0}
        response = "Sure! Let's start with your name. What should I call you?"

    # Check if the user wants to see the list of app users
    elif "app users" in user_message:
        # Fetch the list of app users from Firestore
        users_ref = db.collection("app_users")
        docs = users_ref.stream()
        users = []

        for doc in docs:
            user_data = doc.to_dict()
            users.append(user_data)

        response = "Here are the app users:\n"
        for user in users:
            response += f"Name: {user['name']}, Address: {user['address']}, Phone: {user['phone']}\n"

    # Weather intent detection
    elif "weather in" in user_message:
        location = user_message.split("weather in")[-1].strip().capitalize()
        response = get_weather_for_location(location)

    elif any(keyword in user_message for keyword in ["time", "current time", "what is the time", "tell me the time"]):
        current_time = datetime.now().strftime("%I:%M %p")
        response = f"The current time is: {current_time}"

    elif any(keyword in user_message for keyword in ["date", "current date", "what is the date", "tell me the date", "day"]):
        current_date = datetime.now().strftime("%Y-%m-%d")
        response = f"Today's date is: {current_date}"

    else:
        # Default chatbot model response
        X = np.array(bag_of_words(user_message, all_words))
        X = torch.from_numpy(X).float()
        output = model(X)
        _, predicted = torch.max(output, dim=0)

        tag = tags[predicted.item()]
        response = get_response(tag)

    return jsonify({"response": response})

@app.route('/users', methods=['GET'])
def list_users():
    users_ref = db.collection("app_users")
    docs = users_ref.stream()
    users = []

    for doc in docs:
        user_data = doc.to_dict()
        users.append(user_data)

    return jsonify({"users": users})

if __name__ == "__main__":
    app.run(debug=True)

