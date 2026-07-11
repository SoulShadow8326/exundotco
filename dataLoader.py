import os
from pymongo import MongoClient
from dotenv import load_dotenv
import json


load_dotenv()

client = MongoClient(os.getenv("mongoclient"))
db = client["Slug-URL-DB"] 
collection = db["Slug-URL-Collection"] 
 
with open("data.json", "r") as file:
    data = json.load(file)

mongo_data = []
for doc in data:
    url = doc["val"]

    if url.startswith("/"):
        url = url[1:]
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    mongo_data.append({
        "slug": doc["_id"],
        "url": url,
        "date_modified": doc["date_modified"]
    })

try:
    collection.insert_many(mongo_data, ordered=False)
except Exception as e:
    print(f"Error occurred while inserting data: {e}")