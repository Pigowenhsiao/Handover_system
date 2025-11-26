"""
設備異常記錄相關端點
"""
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from datetime import datetime

from backend import crud, models, schemas
from backend.api.deps import get_db, get_current_active_user
from backend.schemas.equipment import EquipmentLogCreate, EquipmentLogUpdate, EquipmentLog


router = APIRouter()


@router.get("/", response_model=List[EquipmentLog])
def read_equipment_logs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    獲取設備異常記錄列表
    """
    logs = crud.get_equipment_logs(db)
    return logs


@router.get("/by-report/{report_id}", response_model=List[EquipmentLog])
def read_equipment_logs_by_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    根據報表ID獲取設備異常記錄
    """
    logs = crud.get_equipment_logs_by_report_id(db, report_id=report_id)
    return logs


@router.post("/", response_model=EquipmentLog)
def create_equipment_log(
    log: EquipmentLogCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    創建設備異常記錄
    """
    try:
        # 驗證必要字段
        if not log.equip_id or not log.description:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="設備ID和異常內容是必填字段"
            )
        
        # 創建設備異常記錄
        db_log = crud.create_equipment_log(db=db, log=log)
        return db_log
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating equipment log: {str(e)}"
        )


@router.put("/{log_id}", response_model=EquipmentLog)
def update_equipment_log(
    log_id: int,
    log_update: EquipmentLogUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    更新設備異常記錄
    """
    try:
        db_log = crud.update_equipment_log(db=db, log_id=log_id, log_update=log_update)
        if not db_log:
            raise HTTPException(status_code=404, detail="Equipment log not found")
        
        return db_log
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating equipment log: {str(e)}"
        )


@router.delete("/{log_id}")
def delete_equipment_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    刪除設備異常記錄
    """
    success = crud.delete_equipment_log(db=db, log_id=log_id)
    if not success:
        raise HTTPException(status_code=404, detail="Equipment log not found")
    return {"message": "Equipment log deleted successfully"}


@router.post("/upload-image/")
async def upload_equipment_image(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    上傳設備異常圖片
    """
    # 定義允許的文件類型
    allowed_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不支援的檔案格式"
        )
    
    # 創建上傳目錄
    upload_dir = "uploads/equipment_images"
    os.makedirs(upload_dir, exist_ok=True)
    
    # 生成唯一的文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    # 保存文件
    with open(file_path, "wb") as buffer:
        import shutil
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "filename": unique_filename,
        "file_path": file_path,
        "message": "圖片上傳成功"
    }