from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.faculty import (
    FacultyCreate,
    FacultyUpdate,
    FacultyResponse
)
from app.services.faculty_service import (
    create_faculty,
    get_faculty,
    get_all_faculty,
    get_faculty_by_department,
    update_faculty,
    delete_faculty
)

router = APIRouter(
    prefix="/faculty",
    tags=["Faculty"]
)


@router.post("/", response_model=FacultyResponse, status_code=201)
def create_faculty_api(
    faculty_data: FacultyCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_faculty(db, faculty_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[FacultyResponse])
def get_all_faculty_api(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_all_faculty(db, skip, limit)


@router.get("/department/{department_id}", response_model=list[FacultyResponse])
def get_faculty_by_department_api(
    department_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_faculty_by_department(
        db, department_id, skip, limit
    )


@router.get("/{faculty_id}", response_model=FacultyResponse)
def get_faculty_api(
    faculty_id: int,
    db: Session = Depends(get_db)
):
    faculty = get_faculty(db, faculty_id)

    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    return faculty


@router.put("/{faculty_id}", response_model=FacultyResponse)
def update_faculty_api(
    faculty_id: int,
    faculty_data: FacultyUpdate,
    db: Session = Depends(get_db)
):
    try:
        faculty = update_faculty(db, faculty_id, faculty_data)

        if not faculty:
            raise HTTPException(status_code=404, detail="Faculty not found")

        return faculty

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{faculty_id}")
def delete_faculty_api(
    faculty_id: int,
    db: Session = Depends(get_db)
):
    try:
        result = delete_faculty(db, faculty_id)

        if not result:
            raise HTTPException(status_code=404, detail="Faculty not found")

        return {"message": "Faculty deleted successfully"}

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))