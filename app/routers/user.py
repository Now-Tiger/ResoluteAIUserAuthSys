from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError

from utils.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_jwt_token, decode_jwt_token, verify_password
from models.user import PasswordUpdater, UserCreate
from models.token import Token, TokenData
from crud.user import change_password_bd_op, create_user, get_user_by_username, get_user_by_email


userRouter = APIRouter(tags=["auth"], prefix="/product")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="product/login")

"""
{
  "first_name": "Swapnil",
  "last_name": "Narwade",
  "username": "NowTiger",
  "password": "tigerpassword",
  "email": "tiger@hotmail.com"
}
"""

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate":  "Bearer"},
#     )
#     try:
#         payload = decode_jwt_token(token)
#         username = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except InvalidTokenError:
#         raise credentials_exception
#     user = get_user_by_username(username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user
# 


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
        secure=True,  # Use in production with HTTPS
        samesite="lax",  # For CSRF protection
    )
    # JSONResponse(status_code=200, content={"message": "Login successful"})   # BUG: does not sets the access_token token in the cookie.
    return Token(access_token=access_token, token_type="bearer")   # Sets the access_token token in the cookie/client


async def get_logged_user(req: Request):
    """Get the username who is set the cookie session"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":  "Bearer"},
    )
    token = req.cookies.get("access_token")
    # if not token:
    #     raise HTTPException(status_code=404, detail="Cookie not found")
    # payload = decode_jwt_token(token)
    # username = payload.get("sub")
    # if not username:
    #     raise credentials_exception
    # return JSONResponse(status_code=200, content={"logged user": username})
    if token:
        # if you have token then you can definitely get the user
        payload = decode_jwt_token(token)
        username = payload.get("sub")
        return username
    else:
        raise credentials_exception


@userRouter.get("/user/me/changePassword")
async def change_my_password(req: Request):
    # if username:
    #     print(username)
    #     true_user = await get_user_by_username(username)
    #     if not true_user :
    #         raise HTTPException(status_code=400, detail="Bad Request")
    #  right_password = (passwords.old_password == true_user["password"])
    #     if right_password:
    #         data = await change_password_bd_op(true_user["username"], passwords)
    #         print(data)
    #         return JSONResponse(status_code=200, content={"message": "Password changed successfully"})
    #     return JSONResponse(status_code=400, content={"message": "Wrong password"})
    # else:
    #     raise HTTPException(status_code=404, detail="Access denied")

    user = await get_current_user(req) 
    if user:
        # exists = await get_user_by_username(username)
        # exists["_id"] = str(exists["_id"])
        return JSONResponse(status_code=200, content={"msg": user})
    else:
        return JSONResponse(status_code=404, content={"msg": "Does not exist"})


async def get_current_user(req: Request) -> str | None:
    token = req.cookies.get("access_token")
    if token:
        payload = decode_jwt_token(token)
        username= payload.get("sub")
        if username:
            exists = await get_user_by_username(username)
            exists["_id"] = str(exists["_id"])
            return exists
    else:
        return None
