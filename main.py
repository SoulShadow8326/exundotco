from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
mongoclient = os.getenv("mongoclient")
client = MongoClient(mongoclient)

print("connected")