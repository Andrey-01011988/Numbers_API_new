from config_data import config

headers = {
    "X-RapidAPI-Key": config.RAPID_API_KEY,
    "X-RapidAPI-Host": config.HOST_API
}

url = "https://" + config.HOST_API

params = {"fragment": "true", "json": "true"}
