import random
import time
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Define locations
locations = ["Patuakhali", "Barishal", "Rangpur", "Dinajpur", "Bhola"]


# Function to generate random weather data
def generate_random_weather_data():
    return {
        "temperature": round(random.uniform(-10, 40), 2),  # Temperature in Celsius
        "humidity": random.randint(10, 100),  # Humidity percentage
        "condition": random.choice(["Sunny", "Cloudy", "Rainy", "Snowy", "Windy"]),
        "wind_speed": round(random.uniform(0, 20), 2),  # Wind speed in km/h
        "precipitation": round(random.uniform(0, 50), 2),  # Precipitation in mm
        "feels_like": round(random.uniform(-15, 45), 2),  # Feels like temperature
        "uv_index": random.randint(0, 11),  # UV index
        "visibility": random.randint(1, 20)  # Visibility in km
    }


# Function to upload weather data to Firestore
def upload_weather_data():
    for location in locations:
        # Generate random forecast data for 5 future timestamps
        forecasts = []
        for i in range(5):
            forecast_time = datetime.now() + timedelta(hours=i * 3)  # 3-hour intervals
            weather_data = generate_random_weather_data()
            weather_data["timestamp"] = forecast_time.isoformat()
            forecasts.append(weather_data)

        # Create or update location document with forecast data
        location_ref = db.collection("weather_updates").document(location)
        location_ref.set({
            "location_name": location,
            "last_updated": datetime.now().isoformat(),
            "forecasts": forecasts
        })
        print(f"Uploaded weather data for {location}")


# Schedule the upload function
upload_interval = 30

while True:
    upload_weather_data()
    print("Waiting for next update...")
    time.sleep(upload_interval)  # Wait for the next update
