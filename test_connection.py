import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
uri = os.getenv('MONGO_URI')
if not uri:
    raise SystemExit('MONGO_URI is not set in .env')

print('Connecting to MongoDB URI:', uri)
client = MongoClient(uri)
print('Databases:', client.list_database_names())
