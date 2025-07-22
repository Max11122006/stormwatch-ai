import rumps
from weather_api import get_weather
from lightning_api import get_lightning

lat, lon = 52.9, 23.5  # Polish–Belarus border


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


class StormWatchApp(rumps.App):
    def __init__(self):
        super(StormWatchApp, self).__init__("⛈️ StormWatch", icon=None, menu=["Refresh"])
        self.title = "⏳"
        self.update_data()
        self.timer = rumps.Timer(self.update_data, 600)  # Every 10 min
        self.timer.start()

    def update_data(self, _=None):
        try:
            weather = get_weather(lat, lon)
            lightning = get_lightning(lat, lon)
            if "main" not in weather:
                self.title = "❌ API error"
                return

            overall, wind, pres, wc, is_thunder, lightning = check_storm_risk(weather, lightning)
            icon = "⚠️" if overall else "✅"
            self.title = f"{icon} {int(wind)}m/s"
            tooltip = (
                f"🌡 {weather['main']['temp']}°C\n"
                f"💨 {wind} m/s\n"
                f"🔽 {pres} hPa\n"
                f"☁️ {', '.join(wc)}\n"
                f"⚡ Lightning: {'Yes' if lightning else 'No'}\n"
                f"{'⚡ Thunderstorm' if is_thunder else ''}\n"
                f"{'⚠️ Storm risk!' if overall else '✅ No storm risk.'}"
            )
            self.menu["Refresh"].title = tooltip
        except Exception as e:
            self.title = "❌ Error"
            self.menu["Refresh"].title = str(e)

    @rumps.clicked("Refresh")
    def manual_refresh(self, _):
        self.update_data()


if __name__ == "__main__":
    StormWatchApp().run()