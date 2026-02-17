from fastapi import APIRouter, Path, Depends, HTTPException
from tasks.schemas import TaskCreateSchema, TaskUpdateSchema, TaskResponseSchema
from fastapi.responses import JSONResponse
from tasks.models import TaskModel
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
router = APIRouter(tags=["Tasks"], prefix="/todo")


@router.get("/tasks", response_model=List[TaskResponseSchema])
async def retrieve_tasks_list(db: Session = Depends(get_db)):
    tasks = db.query(TaskModel).all()
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskResponseSchema)
async def retrieve_task_detail(task_id: int = Path(..., description="ID of the task to retrieve"), db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/tasks", response_model=TaskResponseSchema)
async def create_task(request: TaskCreateSchema, db: Session = Depends(get_db)):
    new_task = TaskModel(
        title=request.title,
        description=request.description,
        due_date=request.due_date,
        status=request.status
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.put("/tasks/{task_id}", response_model=TaskResponseSchema)
async def update_task(task_id: int = Path(..., description="ID of the task to update"), request: TaskUpdateSchema = None, db: Session = Depends(get_db)):
    task_model = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task_model:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(task_model, field, value)
    db.commit()
    db.refresh(task_model)
    return task_model

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int = Path(..., description="ID of the task to delete"), db: Session = Depends(get_db)):
    task_model = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task_model:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task_model)
    db.commit()
    return JSONResponse(content={"detail": "Task deleted successfully"}, status_code=200)