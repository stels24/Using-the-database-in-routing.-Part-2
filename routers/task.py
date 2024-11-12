from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated

from models.task import Task
from models.user import User
from schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify


router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all_tasks")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks




@router.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User was not found")
    return task




@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], crt_task: CreateTask):
    user = db.scalar(select(User).where(User.id == crt_task.user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User was not found")

    db.execute(insert(Task).values(title=crt_task.title,
                                   content=crt_task.content,
                                   user_id=crt_task.user_id,
                                   slug=slugify(crt_task.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}




@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], user_id: int, upd_task: UpdateTask):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User was not found")

    db.execute(update(Task).where(Task.user_id == user_id).values(title=upd_task.title,
                                                                  content=upd_task.content,
                                                                  user_id=upd_task.user_id,
                                                                  slug=slugify(upd_task.title)))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'User has been updated successfully!'}




@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    user = db.scalar(select(Task).where(Task.id == task_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task was not found")

    db.execute(delete(Task).where(Task.id == task_id))

    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Task has been deleted successfully!'}