import pymongo
from pymongo import MongoClient

def get_mongo_db():
    try:
        # Replace with your MongoDB connection URI
        mongo_uri = "mongodb://username:password@localhost:27017/mydatabase"

        # Create a MongoClient and retrieve the database
        client = MongoClient(mongo_uri)
        database = client.get_database()

        return database

    except Exception as e:
        # Handle any exceptions that may occur during database connection
        print(f"Error connecting to MongoDB: {e}")
        return None
