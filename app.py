import os
import tweepy
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API setup
client = tweepy.Client(
    bearer_token=os.getenv('BEARER_TOKEN'),
    consumer_key=os.getenv('CONSUMER_KEY'),
    consumer_secret=os.getenv('CONSUMER_SECRET'),
    access_token=os.getenv('ACCESS_TOKEN'),
    access_token_secret=os.getenv('ACCESS_TOKEN_SECRET')
)

# Weather API setup
API_KEY = os.getenv('API_WEATHER_KEY')  # OpenWeather API Key

# City to fetch weather data for
city = os.getenv('CITY')

# Fetch weather data
url = f"https://api.openweathermap.org/data/2.5/weather?q={city},PT&appid={API_KEY}&units=metric&lang=en"
res = requests.get(url)

if res.status_code != 200:
    print(f"❌ Error fetching weather data for {city}: {res.status_code} - {res.text}")
else:
    data = res.json()
    city_name = data['name']
    description = data['weather'][0]['description'].capitalize()
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    sunrise = datetime.utcfromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')
    sunset = datetime.utcfromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')

    # Prepare tweet content
    tweet_content = (
        f"🌍 Weather Update for **{city_name}**, Portugal 🇵🇹\n"
        f"🌡️ Temp: {temp:.0f}°C (Feels like {feels_like:.0f}°C)\n"
        f"💧 Humidity: {humidity}%\n"
        f"💨 Wind Speed: {wind_speed} m/s\n"
        f"☀️ Sunrise: {sunrise} UTC\n"
        f"🌇 Sunset: {sunset} UTC\n"
        f"☁️ Condition: {description}\n"
    )

    # Check the length of the tweet content
    if len(tweet_content) > 280:
        tweet_content = tweet_content[:277] + "..."  # Truncate if necessary

    # Send Tweet
    try:
        response = client.create_tweet(text=tweet_content)
        print("✅ Tweet posted successfully!")
    except Exception as e:
        print("❌ Error posting tweet:", e)