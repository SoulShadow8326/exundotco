from pymongo import MongoClient
from dotenv import load_dotenv
import time
import os
load_dotenv()
mongoclient = os.getenv("mongoclient")
client = MongoClient(mongoclient)

print("connected")

class Link:

    def __init__(self, slug, url): #Slug Is Short Link #Url IS The link we need to DIrect User to
                                   #Self Is the main Link we're Making
        self.slug = slug
        self.url = url

    def save(self): #Call it to save the newly made links to DB
        db = client[""] #Name of DB
        collection = db[""] # Name of whatever collection has links.
        try:
            collection.insert_one({
            "slug": self.slug,
            "url": self.url,
            "date_modified": time.time()
            })
        except Exception as e:
            print(e)
            return False
        return True
    
    def delete(self): #Call it to delete the link from DB
        db = client[""] #Name of DB
        collection = db[""] # Name of whatever collection has links.
        try:
            collection.delete_one({"slug": self.slug})
        except Exception as e:
            print(e)
            return False
        return True
   
#Use my Link Class

link = Link(
    "slug",
    
    "main Url"

)