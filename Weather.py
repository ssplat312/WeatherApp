import requests
from dotenv import load_dotenv
import os

def Get5DayForcast(laditude, longitude):
    load_dotenv()

    url = os.environ.get("WeatherUrl")

    querystring = {"lat":laditude,"lon":longitude,"units":"metric","lang":"en"}

    headers = {
        "x-rapidapi-key": os.environ.get("WeatherKey"),
        "x-rapidapi-host": os.environ.get("WeatherHost")
    }
    response = requests.get(url, headers=headers, params=querystring)
    if(response.status_code != 200):
        print(f"Error: code {response.status_code}")
        return None
    

    return response.json()