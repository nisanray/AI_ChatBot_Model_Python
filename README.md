# Weather and Chatbot Application

This application provides a chatbot that can respond to user queries, fetch real-time weather data, and collect user information. Users can either integrate the provided API into their own applications or websites, or use the provided Flutter application for the UI.

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Setup](#setup)
    1. [Clone the Repository](#clone-the-repository)
    2. [Create a Virtual Environment](#create-a-virtual-environment)
    3. [Install Dependencies](#install-dependencies)
    4. [Set up Firebase](#set-up-firebase)
    5. [Train the Model](#train-the-model)
    6. [Prepare Model and Data Files](#prepare-model-and-data-files)
4. [Running the Application](#running-the-application)
5. [API Endpoints](#api-endpoints)
    1. [Chatbot Response](#chatbot-response)
    2. [List Users](#list-users)
6. [Firebase Service Account Key](#firebase-service-account-key)
7. [Using the API in Your Application](#using-the-api-in-your-application)
8. [Flutter Chatbot Integration](#flutter-chatbot-integration)
9. [Specific Formats for User Queries](#specific-formats-for-user-queries)
10. [License](#license)

## Features

- **Weather Data Retrieval**: Fetch real-time weather data from Firestore for a specified location.
- **User Information Collection**: Collect and store user information (name, address, phone number) in Firestore.
- **Chatbot Responses**: Respond to user queries using a trained neural network model.
- **Time and Date Information**: Provide current time and date information upon request.
- **List App Users**: Retrieve and display a list of app users stored in Firestore.

## Requirements

- Python 3.7+
- Flask
- Firebase Admin SDK
- PyTorch
- NumPy

## Setup

### Clone the Repository

1. **Clone the repository**:
    ```sh
    git clone https://github.com/nisanray/AI_ChatBot_Model_Python
    cd AI_ChatBot_Model_Python 
    ```

### Create a Virtual Environment

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

### Install Dependencies

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

### Set up Firebase

4. **Set up Firebase**:
    - Download your Firebase service account key and save it as `serviceAccountKey.json` in the project root directory.
    - Ensure your Firestore database is set up with the required collections (`weather_updates`, `app_users`).

### Train the Model

5. **Train the model**:
    - Run the `train.py` script to train the neural network model and generate `model.pth`:
    ```sh
    python train.py
    ```

### Prepare Model and Data Files

6. **Prepare model and data files**:
    - Ensure `model.pth`, `intents.json`, and `train_data.json` are in the project root directory.

## Running the Application

1. **Start the Flask server**:
    ```sh
    python app.py
    ```

2. **Access the application**:
    - The application will be running at `http://127.0.0.1:5000/`.

## API Endpoints

### Chatbot Response

- **Chatbot Response**: `/chatbot` (POST)
    - Request:
        ```json
        {
            "message": "your message here",
            "user_id": "optional user id"
        }
        ```
    - Response:
        ```json
        {
            "response": "chatbot response here"
        }
        ```

### List Users

- **List Users**: `/users` (GET)
    - Response:
        ```json
        {
            "users": [
                {
                    "user_id": "user id",
                    "name": "user name",
                    "address": "user address",
                    "phone": "user phone",
                    "timestamp": "timestamp"
                },
               "..."
            ]
        }
        ```

## Firebase Service Account Key

You can find the Firebase service account key by following these steps:

1. Go to the [Firebase Console](https://console.firebase.google.com/).
2. Select your project.
3. Click on the gear icon next to "Project Overview" and select "Project settings".
4. Navigate to the "Service accounts" tab.
5. Click on "Generate new private key".
6. A JSON file containing your service account key will be downloaded. Save this file as `serviceAccountKey.json` in the root directory of your project.

Make sure to keep this file secure and do not share it publicly.

## Using the API in Your Application

You can use the provided API endpoints to integrate the chatbot and weather functionalities into your own application or website.

1. **Chatbot Response**: Send a POST request to `/chatbot` with a JSON payload containing the user's message.
2. **List Users**: Send a GET request to `/users` to retrieve a list of app users.

Example using `requests` library in Python:

```python
import requests

# Chatbot response
response = requests.post('http://127.0.0.1:5000/chatbot', json={"message": "Hello"})
print(response.json())

# List users
response = requests.get('http://127.0.0.1:5000/users')
print(response.json())
```

## Flutter Chatbot Integration

To integrate this application with a Flutter frontend, follow these steps:

1. **Clone the Flutter repository**:
    ```sh
    git clone https://github.com/nisanray/FLutter-Chatbot-with-Python.git
    cd FLutter-Chatbot-with-Python
    ```

2. **Install Flutter dependencies**:
    ```sh
    flutter pub get
    ```

3. **Update the API endpoint**:
    - Open the Flutter project and update the API endpoint in the code to point to your Flask server (e.g., `http://127.0.0.1:5000/`).

4. **Run the Flutter application**:
    ```sh
    flutter run
    ```

## Specific Formats for User Queries

To get specific responses from the chatbot, use the following formats:

- **Storing User Information**:
    - Start the process by sending: `"store my info"`
    - Follow the prompts to provide your name, address, and phone number.
    - Confirm by replying `"yes"`.

- **Fetching Weather Data**:
    - Send a message in the format: `"weather in [location]"` (e.g., `"weather in New York"`).

- **Getting Current Time**:
    - Send a message containing any of the following keywords: `"time"`, `"current time"`, `"what is the time"`, `"tell me the time"`.

- **Getting Current Date**:
    - Send a message containing any of the following keywords: `"date"`, `"current date"`, `"what is the date"`, `"tell me the date"`, `"day"`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.#
