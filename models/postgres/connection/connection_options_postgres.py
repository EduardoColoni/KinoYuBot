import os
from dotenv import load_dotenv

load_dotenv()

connection_options_postgres = {
    'HOST': os.getenv('DB_HOST'),
    'PORT': int(os.getenv('DB_PORT', 5432)),
    'USER': os.getenv('DB_USER'),
    'PASSWORD': os.getenv('DB_PASSWORD'),
    'DB_NAME': os.getenv('DB_NAME'),
}