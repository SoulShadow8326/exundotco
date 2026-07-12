from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from dotenv import load_dotenv
from flask import jsonify, request,Flask,render_template,redirect,abort
import time
import os
load_dotenv()

app = Flask(__name__)

mongoclient = os.getenv("mongoclient")
print(mongoclient)
client = MongoClient(mongoclient)

print("connected")

db = client["Slug-URL-DB"] # WARNING: FOR NOW THIS IS JUST HARDCODED FOR MY TESTING CHANGE IT ACCORDING TO YOUR TESTING ENV
collection = db["Slug-URL-Collection"] # WARNING: FOR NOW THIS IS JUST HARDCODED FOR MY TESTING CHANGE IT ACCORDING TO YOUR TESTING ENV
collection.create_index("slug", unique=True)


@app.errorhandler(404)
def not_found(_):
    return render_template("404/404.html"), 404

@app.errorhandler(500)
def internal_error(_):
    return render_template("500/500.html"), 500

class Link:
    @classmethod
    def getBySlug(cls, slug): #Call it to get the link from DB
        
            result = collection.find_one({"slug": slug})
            return result
        
    @classmethod
    def create(cls, slug, url): #Call it to save the newly made links to DB
            collection.insert_one({
            "slug": slug,
            "url": url,
            "date_modified": time.time()
            })
            
    
    @classmethod
    def deleteBySlug(cls, slug): #Call it to delete the link from DB
            result = collection.delete_one({"slug": slug})
            return result
    
    @classmethod
    def updateBySlug(cls, slug, new_slug, new_url): #Call it to update the link in DB
            result = collection.update_one({"slug": slug}, {"$set": {"slug": new_slug, "url": new_url, "date_modified": time.time()}})
            return result
    @classmethod
    def getAll(cls): #Call it to get all the links from DB
        try:
            result = collection.find({},{"_id":0})
            return list(result)
        except Exception as e:
            print(e)
            return []
   
@app.route("/api/create", methods=["POST"])
def create_link():
    data = request.get_json() or {}

    slug = data.get("slug") 
    url = data.get("url") 

    if not slug or not url:
        return jsonify({"success": False, "message": "Slug and URL are required."}), 400

    try:
        Link.create(slug, url)
        return jsonify({"success": True, "message": "Link created successfully."}), 200
    except DuplicateKeyError:
        return jsonify({"success": False, "message": "Slug already exists."}), 409
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "Failed to create link. Internal server error."}), 500

@app.route("/api/delete", methods=["DELETE"])
def delete_link():
    data = request.get_json() or {}

    slug = data.get("slug") 

    if not slug:
        return jsonify({"success": False, "message": "Slug is required."}), 400

    try:
        result = Link.deleteBySlug(slug)
        if result.deleted_count == 0:
            return jsonify({"success": False, "message": "Slug not found."}), 404
        return jsonify({"success": True, "message": "Link deleted successfully."}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "Failed to delete link. Internal server error."}), 500

@app.route("/api/update", methods=["PUT"])
def update_link():
    data = request.get_json() or {}

    slug = data.get("slug") 
    new_slug = data.get("new_slug") 
    new_url = data.get("new_url") 

    if not slug or not new_slug or not new_url:
        return jsonify({"success": False, "message": "All fields are required."}), 400

    try:
        result = Link.updateBySlug(slug, new_slug, new_url)
        if result.matched_count == 0:
            return jsonify({"success": False, "message": "Slug not found."}), 404
        return jsonify({"success": True, "message": "Link updated successfully."}), 200
    except DuplicateKeyError:
        return jsonify({"success": False, "message": "New slug already exists."}), 409
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "Failed to update link. Internal server error."}), 500

@app.route("/api/getAll", methods=["GET"])
def get_all_links():
    try:
        links = Link.getAll()
        return jsonify({"success": True, "links": links}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "Failed to retrieve links. Internal server error."}), 500

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard/dashboard.html")
@app.route("/")
def redir_to_exunclan():
    return redirect("https://exunclan.com")

@app.route("/<path:slug>")
def redirect_slug(slug):
    print("redirect route reached")
    print(slug)
    link = Link.getBySlug("/" +slug)
    print("link: ", link)
    if link is None:
        abort(404)
    return redirect(link["url"])
        



if __name__ == "__main__":
    app.run(debug=True,)
