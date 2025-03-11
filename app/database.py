import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGODB_URI")

# Create the async Motor client
client = AsyncIOMotorClient(uri)

# Access the database
db = client["athmick"]
