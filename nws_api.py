import requests
from datetime import datetime

HEADERS = {
    'User-Agent': 'wind-alert-bot (your@email.com)'  # ← Use your real email
}


def get_point_info(lat, lon):
    url = f"https://api.weather.gov/points/{lat},{lon}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()["properties"]


def get_forecast_summary(lat, lon):
    url = get_point_info(lat, lon)["forecast"]
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    periods = r.json()["properties"]["periods"]

    days = []
    for i in range(0, len(periods), 2):  # Day/Night pairs
        try:
            day = periods[i]
            night = periods[i + 1]
            high = day.get("temperature")
            low = night.get("temperature")
            wind = day.get("windSpeed", "")
            name = day.get("name")
            days.append(f"{name}: High {high}°F / Low {low}°F — Wind: {wind}")
        except:
            continue
    return "7-day forecast:\n" + "\n".join(days[:7])


def get_current_conditions(lat, lon):
    grid = get_point_info(lat, lon)
    obs_url = grid["observationStations"]
    stations = requests.get(obs_url, headers=HEADERS).json()["features"]
    station_url = stations[0]["id"] + "/observations/latest"

    r = requests.get(station_url, headers=HEADERS)
    r.raise_for_status()
    data = r.json()["properties"]

    temp = data["temperature"]["value"]
    wind = data["windSpeed"]["value"]
    precip = data["precipitationLastHour"]["value"]

    return (
        f"🌡 Temp: {round(temp * 9/5 + 32)}°F\n"
        f"💨 Wind: {round(wind * 2.237)} mph\n"
        f"🌧 Rain (last hr): {precip or 0:.2f} mm"
    )


def get_alerts(lat, lon):
    r = requests.get(f"https://api.weather.gov/alerts/active?point={lat},{lon}", headers=HEADERS)
    r.raise_for_status()
    alerts = r.json()["features"]
    if not alerts:
        return "✅ No active alerts."
    return "\n".join([f"🚨 {a['properties']['headline']}" for a in alerts])


def get_hourly_forecast(lat, lon):
    url = get_point_info(lat, lon)["forecastHourly"]
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    periods = r.json()["properties"]["periods"][:6]  # Next 6 hours
    return "\n".join([f"{p['startTime'][11:16]}: {p['temperature']}°F, {p['shortForecast']}, Wind {p['windSpeed']}" for p in periods])


def get_sunrise_sunset(lat, lon):
    forecast = get_point_info(lat, lon)["forecast"]
    r = requests.get(forecast, headers=HEADERS)
    r.raise_for_status()
    periods = r.json()["properties"]["periods"]
    first = periods[0]["detailedForecast"]
    return f"🔆 Based on forecast: {first}"  # We could improve this later with sunrise APIs


def handle_weather_command(command, lat, lon):
    cmd = command.lower()
    if cmd == "forecast":
        return get_forecast_summary(lat, lon)
    elif cmd == "wind now":
        return get_current_conditions(lat, lon).splitlines()[1]
    elif cmd == "temp now":
        return get_current_conditions(lat, lon).splitlines()[0]
    elif cmd == "rain today":
        return get_current_conditions(lat, lon).splitlines()[2]
    elif cmd == "alert":
        return get_alerts(lat, lon)
    elif cmd == "hourly":
        return get_hourly_forecast(lat, lon)
    elif cmd in ["sunrise", "sunset"]:
        return get_sunrise_sunset(lat, lon)
    else:
        return "🤖 Unknown weather command. Try: forecast, wind now, temp now, rain today, alert, hourly, sunrise, sunset."
