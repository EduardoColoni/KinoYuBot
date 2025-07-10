import os
from dotenv import load_dotenv

load_dotenv()

connection_options_postgres = {
    'HOST': os.getenv('DB_HOST', 'localhost'),
    'PORT': int(os.getenv('DB_PORT', 5432)),
    'USER': os.getenv('DB_USER', 'postgres'),
    'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
    'DB_NAME': os.getenv('DB_NAME', 'postgres'),
}