"""
多語言相關端點
"""
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from datetime import datetime

from backend import crud
from backend.database.session import get_db
from backend.models.all_models import User
from backend.schemas.language import (
    LanguageResourceResponse,
    LanguageResourceCreate,
    LanguageResourceUpdate,
    LanguageSettingResponse,
    LanguageSettingUpdate,
    LanguageResourcesResponse
)
from backend.api.deps import get_current_active_superuser, get_current_active_user


router = APIRouter()


@router.get("/resources", response_model=List[LanguageResourceResponse])
def read_language_resources(
    language_code: str,
    namespace: str = "common",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    獲取指定語言和命名空間的翻譯資源
    """
    # 驗證語言代碼是否支援
    if language_code not in ["ja", "zh", "en"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支援的語言代碼: {language_code}，支援的語言: ja, zh, en"
        )
    
    # 獲取語言資源
    resources = crud.get_language_resources_by_language_and_namespace(db, language_code, namespace)
    return resources


@router.get("/resources-full", response_model=LanguageResourcesResponse)
def read_full_language_resources(
    language_code: str,
    namespace: str = "common",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    獲取指定語言和命名空間的完整翻譯資源（巢狀結構）
    """
    # 驗證語言代碼是否支援
    if language_code not in ["ja", "zh", "en"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支援的語言代碼: {language_code}，支援的語言: ja, zh, en"
        )
    
    # 獲取完整語言資源（轉換為巢狀結構）
    resources = crud.get_all_language_resources_by_language_and_namespace(db, language_code, namespace)
    
    # 將扁平結構轉換為巢狀結構
    nested_resources = {}
    for resource in resources:
        # 分割資源鍵為巢狀路徑 (如: header.title -> {header: {title: value}})
        keys = resource.resource_key.split('.')
        current_dict = nested_resources
        
        for key in keys[:-1]:
            if key not in current_dict:
                current_dict[key] = {}
            current_dict = current_dict[key]
        
        current_dict[keys[-1]] = resource.resource_value
    
    return LanguageResourcesResponse(
        lang=language_code,
        namespace=namespace,
        resources=nested_resources
    )


@router.post("/resources", response_model=LanguageResourceResponse)
def create_language_resource(
    resource: LanguageResourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    創建語言資源 (僅管理員)
    """
    # 驗證語言代碼
    if resource.language_code not in ["ja", "zh", "en"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支援的語言代碼: {resource.language_code}，支援的語言: ja, zh, en"
        )
    
    # 驗證資源鍵格式
    if len(resource.resource_key) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="資源鍵長度不能超過255個字符"
        )
    
    try:
        # 檢查資源是否已存在
        existing_resource = crud.get_language_resource_by_key(
            db, 
            language_code=resource.language_code, 
            resource_key=resource.resource_key,
            namespace=resource.namespace
        )
        
        if existing_resource:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="相同語言、鍵和命名空間的翻譯資源已存在"
            )
        
        # 創建語言資源
        db_resource = crud.create_language_resource(db=db, resource=resource)
        return db_resource
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"創建語言資源時發生錯誤: {str(e)}"
        )


@router.put("/resources/{resource_id}", response_model=LanguageResourceResponse)
def update_language_resource(
    resource_id: int,
    resource_update: LanguageResourceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    更新語言資源 (僅管理員)
    """
    try:
        db_resource = crud.update_language_resource(db=db, resource_id=resource_id, resource_update=resource_update)
        if not db_resource:
            raise HTTPException(status_code=404, detail="語言資源不存在")
        
        return db_resource
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新語言資源時發生錯誤: {str(e)}"
        )


@router.delete("/resources/{resource_id}")
def delete_language_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    刪除語言資源 (僅管理員)
    """
    success = crud.delete_language_resource(db=db, resource_id=resource_id)
    if not success:
        raise HTTPException(status_code=404, detail="語言資源不存在")
    return {"message": "語言資源已成功刪除"}


@router.get("/settings", response_model=LanguageSettingResponse)
def read_language_setting(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    獲取當前用戶的語言設定
    """
    setting = crud.get_user_language_setting(db, current_user.id)
    if not setting:
        # 如果用戶沒有語言設定，返回系統默認設定
        setting = crud.get_system_default_language_setting(db)
        if not setting:
            # 如果系統沒有默認設定，返回日文作為默認值
            setting = {
                "user_id": None,
                "language_code": "ja",
                "is_default": True,
                "is_active": True,
                "id": 0,
                "created_at": None,
                "updated_at": None
            }
    
    return setting


@router.put("/settings", response_model=LanguageSettingResponse)
def update_language_setting(
    setting_update: LanguageSettingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    更新用戶的語言設定
    """
    # 驗證語言代碼
    if setting_update.language_code and setting_update.language_code not in ["ja", "zh", "en"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支援的語言代碼: {setting_update.language_code}，支援的語言: ja, zh, en"
        )
    
    try:
        # 更新語言設定
        updated_setting = crud.update_user_language_setting(
            db=db, 
            user_id=current_user.id, 
            language_code=setting_update.language_code
        )
        return updated_setting
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新語言設定時發生錯誤: {str(e)}"
        )