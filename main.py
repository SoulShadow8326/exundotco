from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from dotenv import load_dotenv
from flask import jsonify, request,Flask,render_template,redirect,abort,session,url_for
from authlib.integrations.flask_client import OAuth
from functools import wraps
import time
import os
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("Missing SECRET_KEY environment variable.")

ALLOWED_EMAIL = "exun@dpsrkp.net"

oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

mongoclient = os.getenv("mongoclient")
print(mongoclient)
client = MongoClient(mongoclient)

print("connected")

db = client["Slug-URL-DB"] # WARNING: FOR NOW THIS IS JUST HARDCODED FOR MY TESTING CHANGE IT ACCORDING TO YOUR TESTING ENV
collection = db["Slug-URL-Collection"] # WARNING: FOR NOW THIS IS JUST HARDCODED FOR MY TESTING CHANGE IT ACCORDING TO YOUR TESTING ENV


def is_logged_in():
    return session.get("email") == ALLOWED_EMAIL


def login_required(api=False):
    def decorator(route):
        @wraps(route)
        def wrapped(*args, **kwargs):
            if is_logged_in():
                return route(*args, **kwargs)
            if api:
                return jsonify({"success": False, "message": "Authentication required."}), 401
            return redirect(url_for("login"))
        return wrapped
    return decorator


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
@login_required(api=True)
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
@login_required(api=True)
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
@login_required(api=True)
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
@login_required(api=True)
def get_all_links():
    try:
        links = Link.getAll()
        return jsonify({"success": True, "links": links}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "Failed to retrieve links. Internal server error."}), 500

@app.route("/dashboard")
@login_required()
def dashboard():
    return render_template("dashboard/dashboard.html")

@app.route("/login")
def login():
    if is_logged_in():
        return redirect("/dashboard")
    return render_template("dashboard/login.html")

@app.route("/auth/google")
def auth_google():
    redirect_uri = url_for("auth_callback", _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/auth/callback")
def auth_callback():
    token = google.authorize_access_token()
    user = token.get("userinfo", {})
    email = user.get("email")

    if email == ALLOWED_EMAIL and user.get("email_verified"):
        session["email"] = email
        return redirect("/dashboard")

    session.clear()
    return redirect(url_for("login"))

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
