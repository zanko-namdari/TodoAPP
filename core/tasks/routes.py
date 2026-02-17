from fastapi import APIRouter, Path, Depends, HTTPException, Query
from tasks.schemas import TaskCreateSchema, TaskUpdateSchema, TaskResponseSchema
from tasks.models import TaskModel
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
from tasks.models import StatusEnum
router = APIRouter(tags=["Tasks"], prefix="/todo")


# Retrieve tasks list (with optional status filter)
@router.get("/tasks", response_model=List[TaskResponseSchema])
async def retrieve_tasks_list(
    status: StatusEnum | None = Query(None, description="Filter tasks by status"),
    db: Session = Depends(get_db)
):
    query = db.query(TaskModel)
    if status:
        query = query.filter(TaskModel.status == status)
    return query.all()

# Retrieve task detail by ID
@router.get("/tasks/{task_id}", response_model=TaskResponseSchema)
async def retrieve_task_detail(
    task_id: int = Path(..., description="ID of the task to retrieve"),
    db: Session = Depends(get_db)
):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task



# Create a new task
@router.post("/tasks", response_model=TaskResponseSchema)
async def create_task(
    request: TaskCreateSchema,
    db: Session = Depends(get_db)
):
    new_task = TaskModel(
        title=request.title,
        description=request.description,
        status=request.status,
        due_date=request.due_date
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# Update an existing task
@router.put("/tasks/{task_id}", response_model=TaskResponseSchema)
async def update_task(
    task_id: int = Path(..., description="ID of the task to update"),
    request: TaskUpdateSchema = None,
    db: Session = Depends(get_db)
):
    task_model = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task_model:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(task_model, field, value)

    db.commit()
    db.refresh(task_model)
    return task_model

# Delete a task
@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(
    task_id: int = Path(..., description="ID of the task to delete"),
    db: Session = Depends(get_db)
):
    task_model = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task_model:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task_model)
    db.commit()
    return