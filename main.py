from pymongo import MongoClient
from dotenv import load_dotenv
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
     collection.insert_one({
      "slug": self.slug,
      "url": self.url})
     
#Use my Link Class

link = Link(

    "slug",

    "main Url"

)