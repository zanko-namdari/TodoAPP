from fastapi import APIRouter, Path

router = APIRouter(tags=["Tasks"], prefix="/todo")


@router.get("/tasks")
async def retrieve_tasks_list():
    return []

@router.get("/tasks/{task_id}")
async def retrieve_task_detail(task_id: int):
    return []


@router.post("/tasks")
async def create_task():
    return []

@router.put("/tasks/{task_id}")
async def update_task(task_id: int = Path(..., description="ID of the task to update")):
    return []

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int = Path(..., description="ID of the task to delete")):
    return []