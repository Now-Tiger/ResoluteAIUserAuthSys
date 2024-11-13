from bson import ObjectId
from fastapi import Request

from database.conf import users_collection
from utils.auth import hash_user_password, decode_jwt_token 
from models.user import UserCreate


async def create_user(user: UserCreate):
    """
    Create a new user given via request body. 
    Save the user data in the database also hash password before saving directly.
    """
    user_dict = user.model_dump()
    user_dict["password"] = hash_user_password(user_dict["password"])
    return await users_collection.insert_one(user_dict)


async def get_user_by_email(email: str):
    """Get user with given email address"""
    return await users_collection.find_one({"email": email})


async def get_user_by_id(user_id: str):
    """Get user with given id"""
    return await users_collection.find_one({"_id": ObjectId(user_id)})


async def get_user_by_username(username: str):
    """Get user with given usrname"""
    return await users_collection.find_one({"username": username})


async def delete_user(user_id: str):
    """Delete user given the id"""
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0


async def change_password_bd_op(username: str, new_password: str):
    """
    Update the password of the user given its username to filter 
    out which user and new password to replace with old one
    """
    filter_query = {"username": username}
    update_data = {"$set": {"password": hash_user_password(new_password)}}
    return await users_collection.update_one(filter_query, update_data)


async def get_current_user(req: Request) -> dict | None:
    """
    Finds the currently logged in user from the jwt access 
    token assigned in the client's cookie session/browsere
    """
    token = req.cookies.get("access_token")
    if token:
        payload = decode_jwt_token(token)
        username= payload.get("sub")
        if username:
            user = await get_user_by_username(username)
            user["_id"] = str(user["_id"])
            return user
    else:
        return None
