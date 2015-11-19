import urllib.request
import urllib.parse
import json


def get_weather(location, temperatureFormat='f'):
    locationIds = []
    with open('city.list.json') as f:
        for line in f:
            jsonLocationData = json.loads(line)
            if location in jsonLocationData.get('name'):
                locationIds.append(jsonLocationData.get('_id'))

    if not locationIds:
        return ("Error: Did not find that location. Try another.")

    # Locations can have multiple IDs in the database. Don't know how to deal
    # with that yet, so we're just picking the first one. Hackish but whatever.
    weatherApiUrl = "http://api.openweathermap.org/data/2.5/weather?id=%s&appid=8cf6a6b3ee896aa25f98ac2427e95fd3" % locationIds[0]

    req = urllib.request.Request(weatherApiUrl)
    with urllib.request.urlopen(req) as response:
        downloadedPage = response.read()

    pageJson = json.loads(downloadedPage.decode('utf-8'))

    mainData = pageJson.get('main')
    temperature = float(mainData.get('temp'))
    temperatureMin = float(mainData.get('temp_min'))
    temperatureMax = float(mainData.get('temp_max'))

    # Convert the temperature to either Celsius or Fahrenheit, or leave it as
    # is (in Kelvin)
    if (temperatureFormat == 'c'):
        temperature = kelvin_to_celsius(temperature)
        temperatureMin = kelvin_to_celsius(temperatureMin)
        temperatureMax = kelvin_to_celsius(temperatureMax)
    elif (temperatureFormat == 'f'):
        temperature = celsius_to_fahrenheit(kelvin_to_celsius(temperature))
        temperatureMin = celsius_to_fahrenheit(kelvin_to_celsius(temperatureMin))
        temperatureMax = celsius_to_fahrenheit(kelvin_to_celsius(temperatureMax))

    windData = pageJson.get('wind')
    windSpeed = float(windData.get('speed'))

    response = "Current temperature is %.2f\u00b0F. Low temperature today is %.2f\u00b0F, and the high is %.2f\u00b0F.\nWind speed is %.2f." % (temperature, temperatureMin, temperatureMax, windSpeed)

    return(response)


def kelvin_to_celsius(temperature):
    return (temperature - 273.15)


def celsius_to_fahrenheit(temperature):
    return ((temperature * 1.8) + 32)
