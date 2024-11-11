from typing import List

from fastapi import APIRouter, HTTPException, Body, status
from starlette.responses import JSONResponse
from models.usermodel import User


users_db = list()

userRouter = APIRouter(tags=["user"], prefix="/system")


@userRouter.get("/users", response_model=List[User])
async def get_users() -> List[User]:
    """Get all the users from the databbase"""
    if not users_db:
        # hitting empty database result into an HTTPException i.e BAD REQ.
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "Empty Database!"})
    return users_db


@userRouter.post("/signup")
async def create_user(body: User = Body(...)) -> JSONResponse:
    # TODO: Connect and save user on MongoDB database/collection
    """Create a single user and update the database"""
    print(body)
    users_db.append(body)
    return JSONResponse({"message": "User created successfully"}, status_code=status.HTTP_201_CREATED)

# TODO:
# 1. Login Endpint <- Get user details: 
# [-] username, password & match with the database, if correct then assign him a jwt token,
#     so user can update password or delete account
# 
