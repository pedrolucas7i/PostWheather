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

# === Example list of European countries with at least 2 main cities ===
countries_districts = {
    'United Kingdom': ['London', 'Manchester'],
    'Germany': ['Berlin', 'Munich'],
    'France': ['Paris', 'Lyon'],
    'Spain': ['Madrid', 'Barcelona'],
    'Italy': ['Rome', 'Milan'],
    'Russia': ['Moscow', 'Saint Petersburg'],
    'Poland': ['Warsaw', 'Kraków'],
    'Portugal': ['Lisbon', 'Porto'],
    'Greece': ['Athens', 'Thessaloniki'],
    'Netherlands': ['Amsterdam', 'Rotterdam']
}

# === Weather Data ===
API_KEY = os.getenv('API_WEATHER_KEY')  # OpenWeather API Key

# Initialize tweet content
tweet_content = "🌍 European Weather Update 🌍\n\n"

# Iterate over the countries and cities to fetch weather
for country, cities in countries_districts.items():
    tweet_content += f"🇪🇺 **Weather in {country}:**\n"
    
    # Iterate over cities in the current country
    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}&units=metric&lang=en"

        # Fetch weather data
        res = requests.get(url)
        data = res.json()

        # Extract weather information
        city_name = data['name']
        description = data['weather'][0]['description'].capitalize()
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        min_temp = data['main']['temp_min']
        max_temp = data['main']['temp_max']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        sunrise = data['sys']['sunrise']
        sunset = data['sys']['sunset']

        # Convert sunrise and sunset from UNIX timestamp to human-readable time
        from datetime import datetime
        sunrise_time = datetime.utcfromtimestamp(sunrise).strftime('%H:%M:%S')
        sunset_time = datetime.utcfromtimestamp(sunset).strftime('%H:%M:%S')

        # Format the tweet for the current city
        city_weather = (
            f"  🏙️ **{city_name}**:\n"
            f"    🌡️ Temp: {temp:.0f}°C (Feels like {feels_like:.0f}°C)\n"
            f"    🌡️ Min/Max Temp: {min_temp:.0f}°C / {max_temp:.0f}°C\n"
            f"    💧 Humidity: {humidity}%\n"
            f"    💨 Wind: {wind} m/s\n"
            f"    ☁️ Condition: {description}\n"
            f"    🌅 Sunrise: {sunrise_time} UTC\n"
            f"    🌇 Sunset: {sunset_time} UTC\n\n"
        )

        tweet_content += city_weather  # Add the city's weather info to the tweet content

    tweet_content += "------------------------------------\n"  # Separator for better readability

    # Avoid making the tweet too large by breaking when the tweet is long
    if len(tweet_content) > 280:
        break

# === Send Tweet ===
try:
    print(tweet_content)
    # Posting the tweet using Twitter API v2 (OAuth 2.0)
    response = client.create_tweet(text=tweet_content)
    print("✅ Tweet posted successfully!")
    print("Response:", response)
except Exception as e:
    print("❌ Error posting tweet:", e)
