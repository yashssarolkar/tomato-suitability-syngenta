import requests

# Define the URL of the FastAPI application
url = "http://127.0.0.1:8000/predict"

# Example input payload
payload = {
    "latitude": 15.0,
    "longitude": 74.5,
    "altitude": 120,
    "temperature": 27.5,
    "rainfall": 1500,
    "humidity": 80,
    "sunlight": 8,
    "pH": 6.5,
    "N": 60,
    "P": 30,
    "K": 40,
    "organic_carbon": 0.5,
    "region": "Southern",
    "soil_type": "Clay",
    "variety": "Heirloom",
    "season": "Summer"
}

# Send POST request
response = requests.post(url, json=payload)

# Print the response
if response.status_code == 200:
    print("Response:", response.json())
else:
    print("Error:", response.status_code, response.text)
