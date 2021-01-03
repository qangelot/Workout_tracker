import requests
from datetime import datetime
import os

GENDER = 'male'
WEIGHT_KG = 80
HEIGHT_CM = 188
AGE = 30

# Getting previously set environment variables (export KEY=value in terminal)
APP_ID = os.environ["NT_APP_ID"]
API_KEY = os.environ["NT_API_KEY"]
exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

sheet_endpoint = os.environ["SHEET_ENDPOINT"]

exercise_text = input("Describe which exercises did you do and for how long: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

# Posting my exercises and params to nutritionix NLP feature
response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()

# Get now date and time in desired format
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# Posting exercises into sheet : date/time, name, duration, and calories burned
for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    # Bearer Auth (stronger)
    headers = {
    "Authorization": f"Bearer {os.environ['TOKEN']}"
    }
    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=headers)

    # Content of the response
    print(sheet_response.text)
