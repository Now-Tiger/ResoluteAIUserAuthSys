from fastapi.responses import JSONResponse
from fastapi import FastAPI
import uvicorn as uv
from routers.user import userRouter

from database.conf import users_collection
from models.user import UserCreate
from utils.auth import hash_user_password


__version__ = "0.0.1"


app = FastAPI(
    title="User Auth System",
    description="""## 🌎 User authentication system implemented using FastAPI & MongoDB""",
    version=__version__,
)

# routers included 
app.include_router(userRouter, prefix="/api/v1")


@app.get("/", tags=["Root"])
async def read_root() -> JSONResponse:
    return JSONResponse(
        {
            "message": "Welcome to user auth project developed using FastAPI  & MongoDB"
        }, 
        status_code=200
    )


@app.on_event("startup")
async def create_initial_user():
    # Check if the users collection is empty
    count = await users_collection.count_documents({})
    if count == 0:
        # If empty, insert the initial user
        initial_user = UserCreate(
            first_name="Michael",
            last_name="Jordan",
            username="airjordan",
            password="MichaelAtNBA",
            email="jordan@gmail.com",
        )
        initial_user_dict = initial_user.model_dump()
        initial_user_dict["password"] = hash_user_password(initial_user_dict["password"])
        await users_collection.insert_one(initial_user_dict)
        print("Initial user created.")
    else:
        print("MongoDB collection is already populated with data.")


if __name__ == "__main__":
    uv.run("main:app", reload=True, port=8080)
