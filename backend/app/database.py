from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL   = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "spotify_churn_db")

# Global client — created once, reused across requests
client = None
db     = None

async def connect_db():
    """Called on app startup — opens MongoDB connection"""
    global client, db
    client = AsyncIOMotorClient(MONGODB_URL)
    db     = client[DATABASE_NAME]
    print(f"✅ Connected to MongoDB: {DATABASE_NAME}")

async def close_db():
    """Called on app shutdown — closes MongoDB connection"""
    global client
    if client:
        client.close()
        print("🔌 MongoDB connection closed")

def get_db():
    """Returns the database instance"""
    return db