from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated

from models.user import User
from models.task import Task
from schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/all_users")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

# ===========================================================


@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User was not found")
    return user

# ===========================================================


@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], crt_user: CreateUser):
    db.execute(insert(User).values(username=crt_user.username,
                                   firstname=crt_user.firstname,
                                   lastname=crt_user.lastname,
                                   age=crt_user.age,
                                   slug=slugify(crt_user.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}

# ===========================================================


@router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, upd_user: UpdateUser):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User was not found")

    db.execute(update(User).where(User.id == user_id).values(username=upd_user.username,
                                                             firstname=upd_user.firstname,
                                                             lastname=upd_user.lastname,
                                                             age=upd_user.age,
                                                             slug=slugify(upd_user.username)))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'User update is successful!'}

# ===========================================================


@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User was not found")

    db.execute(delete(Task).where(Task.user_id == user_id))
    db.execute(delete(User).where(User.id == user_id))

    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'User delete is successful!'}

# ===========================================================


@router.get('/user_id/tasks')
async def tasks_by_user_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User was not found')

    db.execute(select(Task).where(Task.user_id == user_id))

    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Successful'}