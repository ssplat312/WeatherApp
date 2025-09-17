from Geolocation import *
from Weather import *
from flask import Flask, render_template, request, jsonify
from waitress import serve
from datetime import timedelta, datetime
app = Flask(__name__)



def ChooseGeoLocation(geolocation):
    curLocationNum = 1
    for location in geolocation["Results"]:
        print(f"{curLocationNum}. address: {location["address"]}\n region: {location["subregion"]}\n country: {location["country"]}")
        curLocationNum = curLocationNum + 1
    choice = -1
    
    while choice < 1 or choice > len(geolocation["Results"]):
        choice = int(input("Which location is the right one?(input here): "))
    
    return geolocation["Results"][choice - 1]

def PrintForcast(allWeather):
    print(f"Weather for {allWeather["city_name"]}, {allWeather["country_code"]}/{allWeather["state_code"]}, Timezone: {allWeather["timezone"]}")
    curDay = 0
    previousDay = curDay
    dayHigh = -1000
    dayLow = 1000
    for weatherData in allWeather["data"]:
        dayPos = weatherData["datetime"].find(":")
        curDay = int(weatherData["datetime"][dayPos - 2:dayPos])
        curTemp =   round(weatherData["temp"], 2)
        if curDay != previousDay:
            print(f"The hgih/low tempeture for day {previousDay} was {dayHigh}C/{dayLow}C or {CelciusToFarinhiet(dayHigh)}F/{CelciusToFarinhiet(dayLow)}F") if previousDay != 0 else print(f"Weather for {curDay} to {curDay + 5}")
            print(f"<br>Weather for day {curDay}.")
            dayHigh = curTemp
            dayLow = curTemp
        print(f"At hour {weatherData["datetime"][dayPos + 1:]} it is {curTemp}C/{CelciusToFarinhiet(curTemp)}F with {weatherData["weather"]["description"]}")
        previousDay = curDay

        if dayHigh < weatherData["temp"]:
            dayHigh = weatherData["temp"]
        elif dayLow > weatherData["temp"]:
            dayLow = weatherData["temp"]
    
    print(f"The hgih/low tempeture for day {previousDay} was {dayHigh}C/{dayLow}C or {CelciusToFarinhiet(dayHigh)}F/{CelciusToFarinhiet(dayLow)}F")
    print("<br><h2>Thats the weather for the next 5 days</h2>")
        

def Get5DayForcastStr(allWeather):
    curDay = 0
    curDayIndex = 0
    previousDay = curDay
    dayHigh = -1000
    dayLow = 1000
    weatherStr = f"<h1>Weather for {allWeather["city_name"]}, {allWeather["country_code"]}/{allWeather["state_code"]}, Timezone: {allWeather["timezone"]}</h1><br>"
    for weatherData in allWeather["data"]:
        dayPos = weatherData["datetime"].find(":")
        curDay = int(weatherData["datetime"][dayPos - 2:dayPos])
        curTemp =   round(weatherData["temp"], 2)
        if curDay != previousDay:
            weatherStr += (f"<b>The hgih/low tempeture for day {previousDay} was {dayLow}C/{dayHigh}C or {CelciusToFarinhiet(dayLow)}F/{CelciusToFarinhiet(dayHigh)}F</b><br>") if previousDay != 0 else (f"<h2>Weather for {GetDatePlusDays(0)} to {GetDatePlusDays(5)}</h2><br>")
            weatherStr += (f"<br><b>Weather for {GetDatePlusDays(curDayIndex)}.</b><br>")
            dayHigh = curTemp
            dayLow = curTemp
            curDayIndex += 1
        weatherStr += (f"At hour {weatherData["datetime"][dayPos + 1:]} it is {curTemp}C/{CelciusToFarinhiet(curTemp)}F with {weatherData["weather"]["description"]}<br>")
        previousDay = curDay
        if dayHigh < weatherData["temp"]:
            dayHigh = weatherData["temp"]
        elif dayLow > weatherData["temp"]:
            dayLow = weatherData["temp"]
    
    weatherStr += (f"<b>The hgih/low tempeture for day {previousDay} was {dayLow}C/{dayHigh}C or {CelciusToFarinhiet(dayLow)}F/{CelciusToFarinhiet(dayHigh)}F</b><br>")
    weatherStr += ("<br><b>Thats the weather for the next 5 days</b><br>")

    return weatherStr

def GetDatePlusDays(dayAmount: int):
    curDate = datetime.now()

    futureDate = curDate + timedelta(days=dayAmount)

    return f"{futureDate.strftime("%B")} {futureDate.day}, {futureDate.year}"

def CelciusToFarinhiet(temputure):
    return round((temputure * 9/5) + 32, 2)

@app.route("/")
def GoMain():
    return render_template("index.html") 

@app.route("/getWeather", methods=["POST"])
def GetWeather():
    locationData = request.get_json()
    stateName = locationData.get("State")
    cityName = locationData.get("City")
    weatherData: str = GetForecastStr(stateName, cityName)
    print(weatherData)
    return jsonify({"WeatherData": weatherData})



def GetForecastStr(stateName, cityName) -> str:
    print(f"Getting Info for {cityName}, {stateName}")
    desiredLocation = cityName + " " + stateName
    GeoLocation = GetGeoLocation(desiredLocation)
    print("Got geolocation")
    selectedLocation = GeoLocation["Results"][0]
    print("Got longitude and laditude")
    WeatherInfo = Get5DayForcast(selectedLocation["latitude"], selectedLocation["longitude"])
    print("Got weather info")
    return Get5DayForcastStr(WeatherInfo)

if __name__ == "__main__":
    
    #desiredLocation = input("Where do you want to check the weather for the next 5 days?(enter the city name and state): ")

    #GeoLocation = GetGeoLocation(desiredLocation)

    #selectedLocation = ChooseGeoLocation(GeoLocation)

    #WeatherInfo = Get5DayForcast(selectedLocation["latitude"], selectedLocation["longitude"])

    #PrintForcast(WeatherInfo)

    serve(app,host="0.0.0.0", port=8000)



