from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.course import (
    CourseCreate,
    CourseUpdate,
    CourseResponse
)

from app.services.course_service import (
    create_course,
    get_course,
    get_all_courses,
    get_courses_by_department,
    update_course,
    delete_course
)

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.post("/", response_model=CourseResponse, status_code=201)
def create_course_api(
    course_data: CourseCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_course(db, course_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[CourseResponse])
def get_all_courses_api(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_all_courses(db, skip, limit)


@router.get("/department/{department_id}", response_model=list[CourseResponse])
def get_courses_by_department_api(
    department_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_courses_by_department(
        db, department_id, skip, limit
    )


@router.get("/{course_id}", response_model=CourseResponse)
def get_course_api(
    course_id: int,
    db: Session = Depends(get_db)
):
    course = get_course(db, course_id)

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


@router.put("/{course_id}", response_model=CourseResponse)
def update_course_api(
    course_id: int,
    course_data: CourseUpdate,
    db: Session = Depends(get_db)
):
    try:
        course = update_course(db, course_id, course_data)

        if not course:
            raise HTTPException(
                status_code=404,
                detail="Course not found"
            )

        return course

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{course_id}")
def delete_course_api(
    course_id: int,
    db: Session = Depends(get_db)
):
    try:
        result = delete_course(db, course_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Course not found"
            )

        return {"message": "Course deleted successfully"}

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))