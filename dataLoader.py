import os
from pymongo import MongoClient
from dotenv import load_dotenv
import json
from pymongo.errors import DuplicateKeyError

load_dotenv()

client = MongoClient(os.getenv("mongoclient"))
db = client["Slug-URL-DB"] 
collection = db["Slug-URL-Collection"] 
 
with open("data.json", "r") as file:
    data = json.load(file)

mongo_data = []
for doc in data:
    mongo_data.append({
        "slug": doc["_id"],
        "url": doc["val"],
        "date_modified": doc["date_modified"]
    })

try:
    collection.insert_many(mongo_data, ordered=False)
except Exception as e:
    print(f"Error occurred while inserting data: {e}")