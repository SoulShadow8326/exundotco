import os

from dotenv import load_dotenv
from pymongo import ASCENDING, MongoClient


name = "Slug-URL-DB"
collection_name = "Slug-URL-Collection"


def main():
    load_dotenv()

    mongo_uri = os.getenv("mongoclient")
    if not mongo_uri:
        raise SystemExit("Missing mongoclient environment variable.")

    client = MongoClient(mongo_uri)
    collection = client[name][collection_name]

    index_name = collection.create_index([("slug", ASCENDING)], unique=True)
    print(f"Ensured unique slug index exists: {index_name}")

    client.close()


if __name__ == "__main__":
    main()
