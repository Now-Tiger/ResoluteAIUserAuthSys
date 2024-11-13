import os
from dotenv import load_dotenv

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Body, FastAPI, HTTPException
import uvicorn as uv

from models.user import User


load_dotenv()
mongo_uri = os.getenv("MONGO_DB_URL")
client = AsyncIOMotorClient(mongo_uri)
database = client["UsersDB"]
users_collection = database["users"]


async def ping_database():
    try:
        await client.admin.command('ping')
        print('successfully connected')
        return
    except Exception as e:
        print(f'Failed to connect: {e}')
        return


app = FastAPI()

# FIX: Alter with fastapi lifespan https://fastapi.tiangolo.com/advanced/events/#lifespan
@app.on_event("startup")
async def startup_db_client():
    await ping_database()


@app.get("/todos")
async def todos():
    todos = await database["todos"].find().to_list()
    if not todos:
        raise HTTPException(status_code=404, detail="Not found")
    for todo in todos:
        todo["_id"] = str(todo["_id"])
    return { "todo": todos }

@app.post("/signup")
async def signup(user: User = Body(...)):
    user_dict = user.model_dump()
    result = await users_collection.insert_one(user_dict)
    if not result:
        raise HTTPException(status_code=500, detail="Server Errir")
    return { "message": "data inserted successfully", "data": user_dict }

@app.get("/users")                                                  
async def users():                                                  
    users = await users_collection.find().to_list()                
    if not users:                                                   
        raise HTTPException(status_code=404, detail="Not found")    
    for user in users:                                              
        user["_id"] = str(user["_id"])                              
    return { "todo": users }                                        



if __name__ == "__main__":
    uv.run('ping:app', reload=True)
