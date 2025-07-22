import subprocess
from lightning_api import get_lightning
from weather_api import get_weather

lat, lon = 52.9, 23.5  # Near Polish–Belarus border

def check_storm_risk(weather, lightning):
    wind = weather['wind']['speed']
    pres = weather['main']['pressure']
    wc = [w['main'].lower() for w in weather['weather']]
    is_thunder = any(200 <= w['id'] < 233 for w in weather['weather'])
    gust_risk = wind > 15
    low_pres = pres < 1000
    lightning_present = len(lightning) > 0
    overall = any([is_thunder, gust_risk, low_pres, lightning_present])
    return overall, wind, pres, wc, is_thunder, lightning_present

def show_popup(title, message):
    script = f'display alert "{title}" message "{message}"'
    subprocess.run(["osascript", "-e", script])
    
def print_summary():
    weather = get_weather(lat, lon)
    lightning = get_lightning(lat, lon)

    if "main" not in weather:
        show_popup("StormWatch AI", "❌ Weather API returned error.")
        return

    overall, wind, pres, wc, is_thunder, light = check_storm_risk(weather, lightning)

    location = weather.get("name", "Unknown")
    temp = weather['main']['temp']
    conditions = ', '.join(wc)

    message = (
        f"📍 {location} ({lat}, {lon})\n"
        f"🌡 {temp}°C\n"
        f"💨 Wind: {wind} m/s\n"
        f"🔽 Pressure: {pres} hPa\n"
        f"☁️ Conditions: {conditions}\n"
        f"⚡ Lightning nearby? {'Yes' if light else 'No'}\n"
        f"{'⚡ Thunderstorm detected!' if is_thunder else ''}\n"
        f"{'⚠️ Storm risk detected!' if overall else '✅ No storm risk.'}"
    )

    show_popup("StormWatch AI", message)

if __name__ == "__main__":
    print_summary()