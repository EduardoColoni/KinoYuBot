import os
from dotenv import load_dotenv

load_dotenv()

discord = {
    'TOKEN': str(os.getenv('DISCORD_TOKEN')),
}

twitch = {
    'CLIENT_ID': str(os.getenv('CLIENT_ID')),
    'CLIENT_SECRET': str(os.getenv('CLIENT_SECRET')),
    'REDIRECT_URI': os.getenv('REDIRECT_URI', 'http://localhost:8000/twitch_callback'),
    'TWITCH_URL' : os.getenv('TWITCH_URL', 'https://id.twitch.tv/oauth2'),
}

connection_options_postgres = {
    'HOST': os.getenv('DB_HOST', 'localhost'),
    'PORT': int(os.getenv('DB_PORT', 5432)),
    'USER': os.getenv('DB_USER', 'postgres' ),
    'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
    'DB_NAME': os.getenv('DB_NAME', 'postgres')
}

connection_options_redis = {
    'HOST': os.getenv('REDIS_HOST', 'localhost'),
    'PORT': int(os.getenv('REDIS_PORT', 6379)),
    'DB': int(os.getenv('REDIS_DB', 0))
}