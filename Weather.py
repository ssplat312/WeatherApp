import requests
def Get5DayForcast(laditude, longitude):
    url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/3hourly"

    querystring = {"lat":laditude,"lon":longitude,"units":"metric","lang":"en"}

    headers = {
        "x-rapidapi-key": "a85dcfd916msh4297cecd3f4bb06p16e23cjsn05408e18591a",
        "x-rapidapi-host": "weatherbit-v1-mashape.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if(response.status_code != 200):
        print(f"Error: code {response.status_code}")
        return None
    

    return response.json()