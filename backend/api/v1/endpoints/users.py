"""
用戶管理端點
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.crud.operations import (
    get_users,
    get_user,
    get_user_by_email,
    get_user_by_username,
    create_user,
    update_user,
    delete_user
)
from backend.database.session import get_db
from backend.models.all_models import User
from backend.schemas.user import UserCreate, UserUpdate, User as UserSchema
from backend.api.deps import get_current_active_superuser
from backend.core.security import get_password_hash


router = APIRouter()


@router.get("/", response_model=List[UserSchema])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    獲取用戶列表
    """
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserSchema)
def create_user_endpoint(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    創建新用戶
    """
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    
    # 創建用戶對象
    hashed_password = get_password_hash(user.password)
    user_in_db = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "role": getattr(user, 'role', 'user'),
        "is_active": getattr(user, 'is_active', True)
    }
    
    db_user = create_user(db=db, user_in_db=user_in_db)
    return db_user


@router.get("/{user_id}", response_model=UserSchema)
def read_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    獲取特定用戶的信息
    """
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserSchema)
def update_user_endpoint(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    更新用戶信息
    """
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 檢查是否提供了新密碼
    if hasattr(user_update, 'password') and user_update.password:
        user_update.hashed_password = get_password_hash(user_update.password)
    
    updated_user = update_user(db=db, db_obj=user, obj_in=user_update)
    return updated_user


@router.delete("/{user_id}")
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    刪除用戶
    """
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    delete_user(db=db, db_obj=user)
    return {"message": f"User {user.username} deleted successfully"}