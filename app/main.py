from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn as uv
from routers.user import userRouter

__version__ = "0.0.1"

app = FastAPI(
    title="User Auth System",
    description="""## User authentication system implemented using FastAPI""",
    version=__version__,
)

# routers included 
app.include_router(userRouter, prefix="/api/v1")

@app.get("/")
async def home() -> JSONResponse:
    return JSONResponse({"message": "Home page"}, status_code=200)


if __name__ == "__main__":
    uv.run("main:app", reload=True)
