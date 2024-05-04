import os
from pathlib import Path

from dotenv import load_dotenv


BaseDir = Path(__file__).parent.parent  # .../src
load_dotenv(Path(BaseDir.parent, '.env'))


HTTP_PROTOCOL = 'http'

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

EXTERNAL_HOST = os.getenv('EXTERNAL_HOST')
EXTERNAL_PORT = int(os.getenv('EXTERNAL_PORT'))

DATABASE = {
    'MIDDLWARE': 'postgresql',
    'USER': os.getenv('DB_USER'),
    'PASSWORD': os.getenv('DB_PASSWORD'),
    'NAME': os.getenv('DB_NAME'),
    'HOST': os.getenv('DB_HOST'),
    'PORT': int(os.getenv('DB_PORT'))
}

TOKEN_SIZE = 48
TOKEN_EXPIRE_TIME = 86400   # In seconds => 1 day


TEST = {
    'DATABASE': {
        'MIDDLWARE': 'postgresql',
        'USER': os.getenv('TEST_DB_USER'),
        'PASSWORD': os.getenv('TEST_DB_PASSWORD'),
        'NAME': os.getenv('TEST_DB_NAME'),
        'HOST': os.getenv('TEST_DB_HOST'),
        'PORT': int(os.getenv('TEST_DB_PORT'))
    }
}


# CORS
ALLOW_ORIGINS = ['*']
ALLOW_CREDENTIALS = False
ALLOW_METHODS = ['*']
ALLOW_HEADERS = ['*']

