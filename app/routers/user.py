from typing import Annotated
from datetime import timedelta
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models.token import Token
from models.user import PasswordUpdater, UserCreate
from utils.auth import create_jwt_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from crud.user import change_password_bd_op, create_user, get_user_by_username, get_user_by_email, get_current_user


userRouter = APIRouter(tags=["auth"], prefix="/product")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="product/login")


@userRouter.post("/signup")
async def signup(user: UserCreate):
    """Create a single user insert details in the database"""
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if existing_user is not None and existing_user["username"] == user.username:
        raise HTTPException(status_code=400, detail="Username is taken!")
    result = await create_user(user)
    if not result:
        raise HTTPException(status_code=500, detail="Internal server error")
    return JSONResponse(status_code=201, content={"message": "User signed up"})
  

@userRouter.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response):
    """
    Verify if the given credentials matches with stored in the database 
    and allow user to login if matches else raises an exception.
    """
    user = await get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=400, 
            detail="Incorrect email or password", 
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_jwt_token(data={"sub": user["username"]}, expires_in=access_token_expires)
    # Set the token as an HTTP-only cookie in the response
    response.set_cookie(
        key="access_token", 
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES,
        secure=True,     # Use in production with HTTPS
        samesite="lax",  # For CSRF protection
    )
    # JSONResponse(status_code=200, content={"message": "Login successful"})   # BUG: does not sets the access_token token in the cookie.
    return Token(access_token=access_token, token_type="bearer")               # Sets the access_token token in the cookie/client


@userRouter.put("/user/me/changePassword")
async def change_my_password(req: Request, passwords: PasswordUpdater):
    """
    User specific action
    ---
    Logged in user can change password.
    If user is not logged in then user is prompted with suitable error information.
    """
    user = await get_current_user(req)
    if user:
        res = verify_password(passwords.old_password, user["password"])
        if res:
            await change_password_bd_op(username=user["username"], new_password=passwords.new_password)
            return JSONResponse(status_code=200, content={"message": "password is changed. Log back again"})
        else:
            return JSONResponse(status_code=401, content={"error": "Incorrect password"})
    else:
        return JSONResponse(status_code=400, content={"error": "You are not logged in!"})
