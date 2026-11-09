from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.lecture_session import (
    LectureSessionCreate,
    LectureSessionUpdate,
    LectureSessionResponse
)

from app.services.lecture_session_service import (
    create_lecture_session,
    get_lecture_session,
    get_all_lecture_sessions,
    get_sessions_by_course,
    get_sessions_by_faculty,
    get_sessions_by_date,
    update_lecture_session,
    delete_lecture_session
)


router = APIRouter(
    prefix="/lecture-sessions",
    tags=["Lecture Sessions"]
)


# CREATE LECTURE SESSION
@router.post(
    "/",
    response_model=LectureSessionResponse,
    status_code=status.HTTP_201_CREATED
)
def create_session(
    session_data: LectureSessionCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_lecture_session(db, session_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# GET ALL LECTURE SESSIONS
@router.get(
    "/",
    response_model=List[LectureSessionResponse]
)
def get_sessions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_all_lecture_sessions(db, skip, limit)


# GET LECTURE SESSION BY ID
@router.get(
    "/{session_id}",
    response_model=LectureSessionResponse
)
def get_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    session = get_lecture_session(db, session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lecture session not found"
        )

    return session


# GET SESSIONS BY COURSE
@router.get(
    "/course/{course_id}",
    response_model=List[LectureSessionResponse]
)
def get_course_sessions(
    course_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_sessions_by_course(db, course_id, skip, limit)


# GET SESSIONS BY FACULTY
@router.get(
    "/faculty/{faculty_id}",
    response_model=List[LectureSessionResponse]
)
def get_faculty_sessions(
    faculty_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_sessions_by_faculty(db, faculty_id, skip, limit)


# GET SESSIONS BY DATE
@router.get(
    "/date/{session_date}",
    response_model=List[LectureSessionResponse]
)
def get_date_sessions(
    session_date: date,
    db: Session = Depends(get_db)
):
    return get_sessions_by_date(db, session_date)


# UPDATE LECTURE SESSION
@router.put(
    "/{session_id}",
    response_model=LectureSessionResponse
)
def update_session(
    session_id: int,
    session_data: LectureSessionUpdate,
    db: Session = Depends(get_db)
):
    try:
        session = update_lecture_session(
            db,
            session_id,
            session_data
        )

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lecture session not found"
            )

        return session

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# DELETE LECTURE SESSION
@router.delete("/{session_id}")
def remove_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    try:
        result = delete_lecture_session(db, session_id)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lecture session not found"
            )

        return {
            "message": "Lecture session deleted successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )