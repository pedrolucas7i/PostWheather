import requests
import tweepy
import os

# === CONFIGURATION ===
# Twitter API credentials
client = tweepy.Client(os.enviroment.get('consumer_key'), os.environment.get('consumer_secret'), os.enviroment.get('access_token'), os.environment.get('access_token_secret'))

# OpenWeather API key
API_KEY = os.environ.get('API_WEATHER_KEY')
city = "London"
country = "uk"  # ISO country code
url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}&units=metric&lang=en"

# === FETCH WEATHER DATA ===
res = requests.get(url)
data = res.json()
print(data)

# === EXTRACT RELEVANT INFO ===
city_name = data['name']
description = data['weather'][0]['description'].capitalize()
temp = data['main']['temp']
feels_like = data['main']['feels_like']
humidity = data['main']['humidity']
wind = data['wind']['speed']

# === FORMAT THE TWEET ===
tweet = (
    f"🌤️ Weather update for {city_name}:\n"
    f"🌡️ {temp:.0f}°C (feels like {feels_like:.0f}°C)\n"
    f"💧 Humidity: {humidity}%\n"
    f"💨 Wind: {wind} m/s\n"
    f"☁️ Condition: {description}\n"
    f"#Weather #Forecast #{city_name.replace(' ', '')}"
)

# === SEND THE TWEET ===
try:
    print(tweet)
    #client.create_tweet(text=tweet)
    print("✅ Tweet posted successfully!")
except Exception as e:
    print("❌ Error posting tweet:", e)
