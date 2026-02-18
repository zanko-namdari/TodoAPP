from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from tasks.routes import router as tasks_router
from users.routes import router as users_router

# 🔹 OpenAPI Tags
tags_metadata = [
    {
        "name": "Tasks",
        "description": "Operations related to task management.",
    },
    {
        "name": "Users",
        "description": "User registration and authentication.",
    },
]


# 🔹 Lifespan events (startup & shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up the application...")
    yield
    print("🛑 Shutting down the application...")


# 🔹 FastAPI App
app = FastAPI(
    title="Task Management API",
    description="API for managing tasks and users.",
    version="1.0.0",
    contact={"name": "zanko"},
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)


# 🔹 Routers
app.include_router(tasks_router)
app.include_router(users_router)


# 🔹 Root endpoint (optional)
@app.get("/")
async def root():
    return {"message": "API is running 🚀"}


from auth.jwt_auth import get_authenticated_user


@app.get("/public")
def public_route():
    return {"message": "This is a public route."}


@app.get("/private")
def private_route(user=Depends(get_authenticated_user)):
    print(user.id)
    return {"message": "This is a private route."}
