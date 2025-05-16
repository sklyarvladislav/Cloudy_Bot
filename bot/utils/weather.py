# utils/weather.py
import aiohttp
from datetime import timedelta, datetime, timezone
from config import WEATHER_API_KEY
from handlers.notification_handler import user_t

greetings = ['Доброе утро', 'Добрый день', 'Добрый вечер', 'Доброй ночи']

def get_greeting(hour: int) -> str:
    if 4 <= hour < 12:
        return greetings[0]
    elif 12 <= hour < 18:
        return greetings[1]
    elif 18 <= hour < 21:
        return greetings[2]
    else:
        return greetings[3]

# Получение погоды по городу
async def get_weather_data_by_city(city: str) -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={WEATHER_API_KEY}"

    # Запрос
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    grinvich_t = datetime.now(timezone.utc)
    local_time = grinvich_t + timedelta(seconds=data['timezone'])

    return {
        'greeting': get_greeting(user_t),
        'city': data['name'],
        'time': local_time.strftime("%H:%M"),
        'temp': round(data['main']['temp']),
        'feels_like': round(data['main']['feels_like']),
        'humidity': data['main']['humidity'],
        'wind': round(data['wind']['speed']),
    }

# Получение погоды по широте и долготе
async def get_weather_data_by_coords(lat: float, lon: float) -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=ru&appid={WEATHER_API_KEY}"

    # Запрос
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    grinvich_t = datetime.now(timezone.utc)
    local_time = grinvich_t + timedelta(seconds=data['timezone'])

    return {
        'greeting': get_greeting(user_t),
        'city': data['name'],
        'time': local_time.strftime("%H:%M"),
        'temp': round(data['main']['temp']),
        'feels_like': round(data['main']['feels_like']),
        'humidity': data['main']['humidity'],
        'wind': round(data['wind']['speed']),
    }
