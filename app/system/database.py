# MongoDB Setup
import os
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "attendance_db")

# mongodb_client = None
# db = None


# async def connect_to_mongo():
#     global mongodb_client, db
#     mongodb_client = AsyncIOMotorClient(MONGODB_URL)
#     db = mongodb_client[DATABASE_NAME]
#     print("✓ Connected to MongoDB")


# async def close_mongo_connection():
#     global mongodb_client
#     if mongodb_client:
#         mongodb_client.close()
#     print("✗ Disconnected from MongoDB")

client = AsyncIOMotorClient(MONGODB_URL)
client.get_io_loop = asyncio.get_event_loop


# Async function to send a ping to confirm a successful connection
def ping_db():
    try:
        # Send a ping to confirm a successful connection
        print("checking connection")
        client.admin.command("ping")
        print("✓ Connected to MongoDB")
    except Exception as e:
        print("✗ Failed to connect to MongoDB")
        raise e


# Async function to get database and collections
db = client.get_database("master")
ping_db()