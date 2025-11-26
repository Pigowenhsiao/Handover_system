"""
異常批次記錄相關端點
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend import crud, models, schemas
from backend.api.deps import get_db, get_current_active_user
from backend.schemas.lot import LotLogCreate, LotLogUpdate, LotLog


router = APIRouter()


@router.get("/", response_model=List[LotLog])
def read_lot_logs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    獲取異常批次記錄列表
    """
    logs = crud.get_lot_logs(db)
    return logs


@router.get("/by-report/{report_id}", response_model=List[LotLog])
def read_lot_logs_by_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    根據報表ID獲取異常批次記錄
    """
    logs = crud.get_lot_logs_by_report_id(db, report_id=report_id)
    return logs


@router.post("/", response_model=LotLog)
def create_lot_log(
    log: LotLogCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    創建異常批次記錄
    """
    try:
        # 驗證必要字段
        if not log.lot_id or not log.description:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="批號和異常內容是必填字段"
            )
        
        # 創建批次記錄
        db_log = crud.create_lot_log(db=db, log=log)
        return db_log
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating lot log: {str(e)}"
        )


@router.put("/{log_id}", response_model=LotLog)
def update_lot_log(
    log_id: int,
    log_update: LotLogUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    更新異常批次記錄
    """
    try:
        db_log = crud.update_lot_log(db=db, log_id=log_id, log_update=log_update)
        if not db_log:
            raise HTTPException(status_code=404, detail="Lot log not found")
        
        return db_log
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating lot log: {str(e)}"
        )


@router.delete("/{log_id}")
def delete_lot_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    刪除異常批次記錄
    """
    success = crud.delete_lot_log(db=db, log_id=log_id)
    if not success:
        raise HTTPException(status_code=404, detail="Lot log not found")
    return {"message": "Lot log deleted successfully"}