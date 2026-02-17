from fastapi import FastAPI
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_router

tags_metadata = [
    {
        "name": "Tasks",
        "description": "Operations related to task management.",
        "externalDocs": {
            "description": "More about Tasks",
            "url": "https://example.com/tasks"
        }
    }

]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up the application...")
    yield
    print("Shutting down the application...")

app = FastAPI(
    title="Task Management API",
    description="API for managing tasks, including creation, retrieval, updating, and deletion.",
    version="0.0.1",
    terms_of_service="https://example.com/terms/",
    contact={
        "name": "zankonamdari",
        "url": "https://varzesh3.com",
        "email": "zankonamdari@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },lifespan=lifespan, openapi_tags=tags_metadata)

app.include_router(tasks_router) 