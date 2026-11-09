from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse
)

from app.services.student_service import (
    create_student,
    get_student,
    get_student_by_enrollment,
    get_all_students,
    get_students_by_department,
    update_student,
    delete_student
)

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post("/", response_model=StudentResponse, status_code=201)
def create_student_api(
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_student(db, student_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[StudentResponse])
def get_all_students_api(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_all_students(db, skip, limit)


@router.get("/enrollment/{enrollment_number}", response_model=StudentResponse)
def get_student_by_enrollment_api(
    enrollment_number: str,
    db: Session = Depends(get_db)
):
    student = get_student_by_enrollment(db, enrollment_number)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@router.get("/department/{department_id}", response_model=list[StudentResponse])
def get_students_by_department_api(
    department_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_students_by_department(
        db, department_id, skip, limit
    )


@router.get("/{student_id}", response_model=StudentResponse)
def get_student_api(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = get_student(db, student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student_api(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db)
):
    try:
        student = update_student(
            db, student_id, student_data
        )

        if not student:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        return student

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{student_id}")
def delete_student_api(
    student_id: int,
    db: Session = Depends(get_db)
):
    try:
        result = delete_student(db, student_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        return {"message": "Student deleted successfully"}

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))