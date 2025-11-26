"""
出勤記錄相關端點
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend import crud, models, schemas
from backend.api.deps import get_db, get_current_active_user
from backend.schemas.attendance import AttendanceRecordCreate, AttendanceRecordUpdate, AttendanceRecord


router = APIRouter()


@router.get("/", response_model=List[AttendanceRecord])
def read_attendance_records(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    獲取出勤記錄列表
    """
    records = crud.get_attendance_records(db)
    return records


@router.get("/by-report/{report_id}", response_model=List[AttendanceRecord])
def read_attendance_records_by_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    根據報表ID獲取出勤記錄
    """
    records = crud.get_attendance_records_by_report_id(db, report_id=report_id)
    return records


@router.post("/", response_model=AttendanceRecord)
def create_attendance_record(
    record: AttendanceRecordCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    創建出勤記錄 - 同時支持正社員和契約社員
    """
    try:
        # 驗證輸入數據
        if record.scheduled_count < 0 or record.present_count < 0 or record.absent_count < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="人數不能為負數"
            )
        
        if record.present_count + record.absent_count > record.scheduled_count:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="出勤人數與缺勤人數總和不能超過定員人數"
            )
        
        db_record = crud.create_attendance_record(db=db, record=record)
        return db_record
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating attendance record: {str(e)}"
        )


@router.put("/{record_id}", response_model=AttendanceRecord)
def update_attendance_record(
    record_id: int,
    record_update: AttendanceRecordUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    更新出勤記錄
    """
    try:
        db_record = crud.update_attendance_record(db=db, record_id=record_id, record_update=record_update)
        if not db_record:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        
        return db_record
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating attendance record: {str(e)}"
        )


@router.delete("/{record_id}")
def delete_attendance_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    刪除出勤記錄
    """
    success = crud.delete_attendance_record(db=db, record_id=record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return {"message": "Attendance record deleted successfully"}