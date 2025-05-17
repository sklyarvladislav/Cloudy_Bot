import os
import toml

config = toml.load(os.getenv("CONFIG_FILE"))

BOT_TOKEN = config["bot"]["BOT_TOKEN"]
WEATHER_API_KEY = config["weather_api"]["WEATHER_API_KEY"]
