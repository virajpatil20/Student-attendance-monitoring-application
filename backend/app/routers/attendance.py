from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse
)
from app.services.attendance_service import (
    create_attendance,
    get_attendance,
    get_all_attendance,
    get_attendance_by_student,
    get_attendance_by_course,
    get_attendance_by_date,
    update_attendance,
    delete_attendance
)

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


@router.post("/", response_model=AttendanceResponse, status_code=201)
def create_attendance_api(
    attendance_data: AttendanceCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_attendance(db, attendance_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[AttendanceResponse])
def get_all_attendance_api(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_all_attendance(db, skip, limit)


@router.get("/student/{student_id}", response_model=list[AttendanceResponse])
def get_attendance_by_student_api(
    student_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_attendance_by_student(
        db, student_id, skip, limit
    )


@router.get("/course/{course_id}", response_model=list[AttendanceResponse])
def get_attendance_by_course_api(
    course_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_attendance_by_course(
        db, course_id, skip, limit
    )


@router.get("/date/{attendance_date}", response_model=list[AttendanceResponse])
def get_attendance_by_date_api(
    attendance_date: date,
    db: Session = Depends(get_db)
):
    return get_attendance_by_date(db, attendance_date)


@router.get("/{attendance_id}", response_model=AttendanceResponse)
def get_attendance_api(
    attendance_id: int,
    db: Session = Depends(get_db)
):
    attendance = get_attendance(db, attendance_id)

    if not attendance:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found"
        )

    return attendance


@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance_api(
    attendance_id: int,
    attendance_data: AttendanceUpdate,
    db: Session = Depends(get_db)
):
    try:
        attendance = update_attendance(
            db, attendance_id, attendance_data
        )

        if not attendance:
            raise HTTPException(
                status_code=404,
                detail="Attendance record not found"
            )

        return attendance

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{attendance_id}")
def delete_attendance_api(
    attendance_id: int,
    db: Session = Depends(get_db)
):
    try:
        result = delete_attendance(db, attendance_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Attendance record not found"
            )

        return {"message": "Attendance deleted successfully"}

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))