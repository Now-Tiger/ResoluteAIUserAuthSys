import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

mongo_uri = os.getenv("MONGO_DB_URL")
client = AsyncIOMotorClient(mongo_uri)
database = client["UsersDB"]
users_collection = database["users"]

