import os
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB Atlas URI (ensure it is set in your environment variables)
uri = os.getenv("MONGODB_URI")

# Create the async Motor client
client = AsyncIOMotorClient(uri)

# Access the database
db = client["athmick"]
