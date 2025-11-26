"""
認證相關端點
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend import crud, models, schemas
from backend.api.deps import get_db, get_current_user
from backend.core.security import create_access_token, verify_password, get_password_hash
from backend.core.config import settings


router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    使用者登入
    """
    user = crud.authenticate_user(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout_user():
    """
    使用者登出
    """
    # 在實際實施中，可能需要在服務器端實現令牌無效化
    # 目前返回成功響應
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    """
    獲取當前使用者資訊
    """
    return current_user