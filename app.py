import requests
import tweepy
import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

# === OAuth 2.0 Authentication with Twitter API ===
client = tweepy.Client(
    access_token=os.getenv('ACCESS_TOKEN'),  # OAuth 2.0 access token
    access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'),  # If you use secret for OAuth 1.0a
    consumer_key=os.getenv('CONSUMER_KEY'),  # Your Consumer Key (API Key)
    consumer_secret=os.getenv('CONSUMER_SECRET')  # Your Consumer Secret (API Secret Key)
)

# === Weather Data ===
API_KEY = os.getenv('API_WEATHER_KEY')  # OpenWeather API Key
city = "London"
country = "uk"
url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}&units=metric&lang=en"

# Fetch weather data
res = requests.get(url)
data = res.json()

# === Extract and format data ===
city_name = data['name']
description = data['weather'][0]['description'].capitalize()
temp = data['main']['temp']
feels_like = data['main']['feels_like']
humidity = data['main']['humidity']
wind = data['wind']['speed']

tweet = (
    f"🌤️ Weather update for {city_name}:\n"
    f"🌡️ {temp:.0f}°C (feels like {feels_like:.0f}°C)\n"
    f"💧 Humidity: {humidity}%\n"
    f"💨 Wind: {wind} m/s\n"
    f"☁️ Condition: {description}\n"
    f"#Weather #Forecast #{city_name.replace(' ', '')}"
)

# === Send Tweet ===
try:
    print(tweet)
    # Posting the tweet using Twitter API v2 (OAuth 2.0)
    response = client.create_tweet(text=tweet)
    print("✅ Tweet posted successfully!")
    print("Response:", response)
except Exception as e:
    print("❌ Error posting tweet:", e)
