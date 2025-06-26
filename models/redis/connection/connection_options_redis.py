import os
from dotenv import load_dotenv

load_dotenv()

connection_options = {
    'HOST': os.getenv('REDIS_HOST'),
    'PORT': os.getenv('REDIS_PORT'),
    'DB': os.getenv('REDIS_DB')
}