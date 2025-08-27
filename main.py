from Geolocation import *
from Weather import *

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
            print(f"\nWeather for day {curDay}.")
            dayHigh = curTemp
            dayLow = curTemp
        print(f"At hour {weatherData["datetime"][dayPos + 1:]} it is {curTemp}C/{CelciusToFarinhiet(curTemp)}F with {weatherData["weather"]["description"]}")
        previousDay = curDay

        if dayHigh < weatherData["temp"]:
            dayHigh = weatherData["temp"]
        elif dayLow > weatherData["temp"]:
            dayLow = weatherData["temp"]
    
    print(f"The hgih/low tempeture for day {previousDay} was {dayHigh}C/{dayLow}C or {CelciusToFarinhiet(dayHigh)}F/{CelciusToFarinhiet(dayLow)}F")
    print("\nThats the weather for the next 5 days")
        

def CelciusToFarinhiet(temputure):
    return round((temputure * 9/5) + 32, 2)

if __name__ == "__main__":

    desiredLocation = input("Where do you want to check the weather for the next 5 days?(enter the city name and state): ")

    GeoLocation = GetGeoLocation(desiredLocation)

    selectedLocation = ChooseGeoLocation(GeoLocation)

    WeatherInfo = Get5DayForcast(selectedLocation["latitude"], selectedLocation["longitude"])

    PrintForcast(WeatherInfo)



