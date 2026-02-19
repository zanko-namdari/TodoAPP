from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from auth.jwt_auth import get_authenticated_user
from core.database import get_db
from tasks.models import StatusEnum, TaskModel
from tasks.schemas import (TaskCreateSchema, TaskResponseSchema,
                           TaskUpdateSchema)
from users.models import UserModel

router = APIRouter(prefix="/todo", tags=["Tasks"])


#  Retrieve tasks list
@router.get("/tasks", response_model=List[TaskResponseSchema])
async def retrieve_tasks_list(
    status_filter: Optional[StatusEnum] = Query(
        None, description="Filter tasks by status"
    ),
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(10, le=100, description="Number of tasks to return"),
    sort_by_due: bool = Query(False, description="Sort by due date"),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    query = db.query(TaskModel).filter(TaskModel.user_id == user.id)

    if status_filter:
        query = query.filter(TaskModel.status == status_filter)

    if sort_by_due:
        query = query.order_by(TaskModel.due_date)

    tasks = query.offset(skip).limit(limit).all()
    return tasks


#  Retrieve task detail
@router.get("/tasks/{task_id}", response_model=TaskResponseSchema)
async def retrieve_task_detail(
    task_id: int = Path(..., description="ID of the task"),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    task = (
        db.query(TaskModel)
        .filter(TaskModel.id == task_id, TaskModel.user_id == user.id)
        .one_or_none()
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


#  Create task
@router.post(
    "/tasks", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_task(
    request: TaskCreateSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    new_task = TaskModel(
        title=request.title,
        description=request.description,
        status=request.status,
        due_date=request.due_date,
        user_id=user.id,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


#  Update task
@router.put("/tasks/{task_id}", response_model=TaskResponseSchema)
async def update_task(
    task_id: int = Path(..., description="ID of the task to update"),
    request: TaskUpdateSchema = ...,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    task_model = (
        db.query(TaskModel)
        .filter(TaskModel.id == task_id, TaskModel.user_id == user.id)
        .one_or_none()
    )

    if not task_model:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(task_model, field, value)

    db.commit()
    db.refresh(task_model)
    return task_model


#  Delete task
@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int = Path(..., description="ID of the task to delete"),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    task_model = (
        db.query(TaskModel)
        .filter(TaskModel.id == task_id, TaskModel.user_id == user.id)
        .one_or_none()
    )

    if not task_model:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task_model)
    db.commit()
