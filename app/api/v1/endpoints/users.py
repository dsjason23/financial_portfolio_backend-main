# api/v1/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import user as schema
from app.services import user as service

router = APIRouter()

@router.post("/")
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    existing_user = await service.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return await service.create_user(db, user)

@router.get("/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = await service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user_update: schema.UserUpdate,
    db: Session = Depends(get_db)
):
    user = await service.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = await service.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User successfully deleted"}