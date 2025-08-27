import requests
from dotenv import load_dotenv
import os

def GetGeoLocation(location):
    load_dotenv()

    url = os.environ.get("GeoloationUrl")

    querystring = {"address": location}


    headers = {
        "x-rapidapi-key": os.environ.get("GeolocationKey"),
        "x-rapidapi-host": os.environ.get("GeolocationHost")
    }

    response = requests.get(url, headers=headers, params=querystring)
    if(response.status_code != 200):
        print(f"Error: code {response.status_code}")
        return None
    
    return response.json()