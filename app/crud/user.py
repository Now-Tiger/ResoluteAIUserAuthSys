from bson import ObjectId

from models.user import PasswordUpdater, UserCreate
from database.conf import users_collection
from utils.auth import hash_user_password 


async def create_user(user: UserCreate):
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


async def change_password_bd_op(username: str, passwords: PasswordUpdater):
    filter_query = {"username": username}
    update_data = {"$set": {"password": passwords.new_password}}
    return await users_collection.update_one(filter_query, update_data)

