import requests

HEADERS = {
    'User-Agent': 'wind-alert-bot ({EMAIL_ADDRESS})'  # Replace with your real email
}

def get_forecast_url(lat, lon):
    """Get the URL for the forecast at the given coordinates."""
    url = f"https://api.weather.gov/points/{lat},{lon}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["properties"]["forecast"]

def get_high_wind_period(lat, lon, threshold=25):
    """Check for any forecast periods with wind speeds above the threshold."""
    forecast_url = get_forecast_url(lat, lon)
    response = requests.get(forecast_url, headers=HEADERS)
    response.raise_for_status()
    periods = response.json()["properties"]["periods"]

    for period in periods:
        wind = period.get("windSpeed", "")
        if "to" in wind:
            # Example: "15 to 25 mph"
            try:
                speed = int(wind.split("to")[-1].split()[0])
            except:
                continue
        else:
            try:
                speed = int(wind.split()[0])
            except:
                continue

        if speed >= threshold:
            return f"⚠️ {period['name']}: {wind} winds. {period['detailedForecast']}"

    return "✅ No high winds forecast in the next few days."
