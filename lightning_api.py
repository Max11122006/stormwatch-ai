import os
import requests
from dotenv import load_dotenv

load_dotenv()
WB_KEY = os.getenv("WEATHERBIT_API_KEY")

def get_lightning(lat, lon, dist_km=50, minutes=30):
    url = (
        f"https://api.weatherbit.io/v2.0/current/lightning"
        f"?key={WB_KEY}&lat={lat}&lon={lon}"
        f"&search_dist_km={dist_km}&search_mins={minutes}"
    )
    resp = requests.get(url)
    data = resp.json()
    if resp.status_code != 200:
        print("⚠️ Lightning API error:", data.get("error"))
        return []
    return data.get("data", [])