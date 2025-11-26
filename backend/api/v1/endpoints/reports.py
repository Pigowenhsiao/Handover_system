"""
日報表相關端點
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from backend import crud
from backend.database.session import get_db
from backend.models.all_models import User
from backend.schemas.report import DailyReportCreate, DailyReportUpdate, DailyReportResponse
from backend.api.deps import get_current_active_user


router = APIRouter()


@router.get("/", response_model=List[DailyReportResponse])
def read_daily_reports(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """
    獲取日報表列表
    """
    reports = crud.get_daily_reports(db, skip=skip, limit=limit)
    return reports


@router.get("/by-date-range", response_model=List[DailyReportResponse])
def read_daily_reports_by_date_range(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    根據日期範圍獲取日報表
    """
    reports = crud.get_daily_reports_by_date_range(db, start_date, end_date)
    if not reports:
        raise HTTPException(status_code=404, detail="No reports found for the specified date range")
    return reports


@router.get("/{report_id}", response_model=DailyReportResponse)
def read_daily_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    獲取特定日報表
    """
    report = crud.get_daily_report(db, report_id=report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.post("/", response_model=DailyReportResponse)
def create_daily_report(
    report: DailyReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    創建新日報表
    """
    try:
        # 使用當前用戶創建日報表
        db_report = crud.create_daily_report(db=db, report=report, author_id=current_user.id)
        return db_report
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating report: {str(e)}"
        )


@router.put("/{report_id}", response_model=DailyReportResponse)
def update_daily_report(
    report_id: int,
    report_update: DailyReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    更新日報表
    """
    try:
        db_report = crud.update_daily_report(db=db, report_id=report_id, report_update=report_update)
        if not db_report:
            raise HTTPException(status_code=404, detail="Report not found")
        return db_report
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating report: {str(e)}"
        )


@router.delete("/{report_id}")
def delete_daily_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    刪除日報表
    """
    try:
        success = crud.delete_daily_report(db=db, report_id=report_id)
        if not success:
            raise HTTPException(status_code=404, detail="Report not found")
        return {"message": "Report deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting report: {str(e)}"
        )