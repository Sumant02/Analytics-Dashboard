import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'sales_db')
COLLECTION_NAME = os.environ.get('COLLECTION_NAME', 'transactions')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
transactions = db[COLLECTION_NAME]
