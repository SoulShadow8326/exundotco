from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from dotenv import load_dotenv
from flask import Flask,render_template,redirect,abort
import time
import os
load_dotenv()

app = Flask(__name__)

mongoclient = os.getenv("mongoclient")
client = MongoClient(mongoclient)

print("connected")

db = client["Slug-URL-DB"] # WARNING: FOR NOW THIS IS JUST HARDCODED FOR MY TESTING CHANGE IT ACCORDING TO YOUR TESTING ENV
collection = db["Slug-URL-Collection"] # WARNING: FOR NOW THIS IS JUST HARDCODED FOR MY TESTING CHANGE IT ACCORDING TO YOUR TESTING ENV
collection.create_index("slug", unique=True)


@app.errorhandler(404)
def not_found(_):
    return render_template("404.html"), 404

class Link:

    # def __init__(self, slug, url): #Slug Is Short Link #Url IS The link we need to DIrect User to
    #                                #Self Is the main Link we're Making
    #     self.slug = slug
    #     self.url = url

    @classmethod
    def getBySlug(cls, slug): #Call it to get the link from DB
        
        try:    
            result = collection.find_one({"slug": slug})
            if result is None:
                print("No doc found with the given slug.")
                return None 
            return result
        except Exception as e:
            print(e)
            return None
        
    @classmethod
    def create(cls, slug, url): #Call it to save the newly made links to DB
        try:
            collection.insert_one({
            "slug": slug,
            "url": url,
            "date_modified": time.time()
            })
        except DuplicateKeyError:
            print("Slug already exists.")
            return False
        except Exception as e:
            print(e)
            return False
        return True
    
    @classmethod
    def deleteBySlug(cls, slug): #Call it to delete the link from DB
        try:
            result = collection.delete_one({"slug": slug})
            if result.deleted_count == 0:
                print("No doc found with the given slug.")
                return False
        except Exception as e:
            print(e)
            return False
        return True
    
    @classmethod
    def updateBySlug(cls, slug, new_slug, new_url): #Call it to update the link in DB
        try:
            result = collection.update_one({"slug": slug}, {"$set": {"slug": new_slug, "url": new_url, "date_modified": time.time()}})
            if result.matched_count == 0:
                print("No doc found with the given slug.")
                return False
        except DuplicateKeyError:
            print("New slug already exists.")
            return False
        except Exception as e:
            print(e)
            return False
        return True
   
@app.route("/<path:slug>")
def redirect_slug(slug):
    print(slug)
    link = Link.getBySlug(slug)

    if link is None:
        abort(404)

    return redirect(link["url"])


if __name__ == "__main__":
    app.run()
