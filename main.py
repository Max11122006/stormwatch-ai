from weather_api import get_weather_data
city = "warsaw"
weather_data = get_weather_data(city)

print(f"Weather in {city.capitalize()}:")
print(f"Temperature: {weather_data['main']['temp']}°C")
print(f"Weather: {weather_data['weather'][0]['description']}")
print(f"pressure: {weather_data['main']['pressure']} hPa")