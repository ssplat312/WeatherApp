import requests
def GetGeoLocation(location):
    url = "https://address-from-to-latitude-longitude.p.rapidapi.com/geolocationapi"

    querystring = {"address": location}

    headers = {
        "x-rapidapi-key": "a85dcfd916msh4297cecd3f4bb06p16e23cjsn05408e18591a",
        "x-rapidapi-host": "address-from-to-latitude-longitude.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if(response.status_code != 200):
        print(f"Error: code {response.status_code}")
        return None
    
    return response.json()