from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.lecture_session import LectureSession
from app.models.course import Course
from app.models.faculty import Faculty
from app.models.attendance import Attendance

from app.schemas.lecture_session import (
    LectureSessionCreate,
    LectureSessionUpdate
)


def create_lecture_session(
    db: Session,
    session_data: LectureSessionCreate
):
    # Verify course exists
    course = db.query(Course).filter(
        Course.id == session_data.course_id
    ).first()

    if not course:
        raise ValueError("Course does not exist")

    # Verify faculty exists and belongs to the course department
    faculty = db.query(Faculty).filter(
        Faculty.id == session_data.faculty_id,
        Faculty.department_id == course.department_id
    ).first()

    if not faculty:
        raise ValueError(
            "Faculty does not belong to the course department"
        )

    # Prevent duplicate lecture numbers for the same course and date
    existing = db.query(LectureSession).filter(
        LectureSession.course_id == session_data.course_id,
        LectureSession.session_date == session_data.session_date,
        LectureSession.lecture_number == session_data.lecture_number
    ).first()

    if existing:
        raise ValueError(
            "This lecture number already exists for this course and date"
        )

    lecture_session = LectureSession(
        **session_data.model_dump()
    )

    try:
        db.add(lecture_session)
        db.commit()
        db.refresh(lecture_session)

    except IntegrityError:
        db.rollback()
        raise ValueError(
            "Could not create lecture session due to a database constraint"
        )

    return lecture_session


def get_lecture_session(
    db: Session,
    session_id: int
):
    return db.query(LectureSession).filter(
        LectureSession.id == session_id
    ).first()


def get_all_lecture_sessions(
    db: Session,
    skip: int = 0,
    limit: int = 100
):
    return db.query(LectureSession).order_by(
        LectureSession.session_date.desc(),
        LectureSession.start_time
    ).offset(skip).limit(limit).all()


def get_sessions_by_course(
    db: Session,
    course_id: int,
    skip: int = 0,
    limit: int = 100
):
    return db.query(LectureSession).filter(
        LectureSession.course_id == course_id
    ).order_by(
        LectureSession.session_date.desc(),
        LectureSession.start_time
    ).offset(skip).limit(limit).all()


def get_sessions_by_faculty(
    db: Session,
    faculty_id: int,
    skip: int = 0,
    limit: int = 100
):
    return db.query(LectureSession).filter(
        LectureSession.faculty_id == faculty_id
    ).order_by(
        LectureSession.session_date.desc(),
        LectureSession.start_time
    ).offset(skip).limit(limit).all()


def get_sessions_by_date(
    db: Session,
    session_date: date
):
    return db.query(LectureSession).filter(
        LectureSession.session_date == session_date
    ).order_by(
        LectureSession.start_time
    ).all()


def update_lecture_session(
    db: Session,
    session_id: int,
    session_data: LectureSessionUpdate
):
    lecture_session = get_lecture_session(db, session_id)

    if not lecture_session:
        return None

    update_data = session_data.model_dump(exclude_unset=True)

    # Calculate final values after applying the update
    course_id = update_data.get(
        "course_id", lecture_session.course_id
    )

    faculty_id = update_data.get(
        "faculty_id", lecture_session.faculty_id
    )

    session_date = update_data.get(
        "session_date", lecture_session.session_date
    )

    lecture_number = update_data.get(
        "lecture_number", lecture_session.lecture_number
    )

    start_time = update_data.get(
        "start_time", lecture_session.start_time
    )

    end_time = update_data.get(
        "end_time", lecture_session.end_time
    )

    # Validate lecture timing
    if end_time <= start_time:
        raise ValueError(
            "End time must be after start time"
        )

    # Verify course
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise ValueError("Course does not exist")

    # Verify faculty belongs to the course department
    faculty = db.query(Faculty).filter(
        Faculty.id == faculty_id,
        Faculty.department_id == course.department_id
    ).first()

    if not faculty:
        raise ValueError(
            "Faculty does not belong to the course department"
        )

    # Check duplicate lecture number
    duplicate = db.query(LectureSession).filter(
        LectureSession.course_id == course_id,
        LectureSession.session_date == session_date,
        LectureSession.lecture_number == lecture_number,
        LectureSession.id != session_id
    ).first()

    if duplicate:
        raise ValueError(
            "This lecture number already exists for this course and date"
        )

    for key, value in update_data.items():
        setattr(lecture_session, key, value)

    try:
        db.commit()
        db.refresh(lecture_session)

    except IntegrityError:
        db.rollback()
        raise ValueError(
            "Could not update lecture session due to a database constraint"
        )

    return lecture_session


def delete_lecture_session(
    db: Session,
    session_id: int
):
    lecture_session = get_lecture_session(db, session_id)

    if not lecture_session:
        return None

    # Prevent deletion if attendance has already been recorded
    existing_attendance = db.query(Attendance).filter(
        Attendance.session_id == session_id
    ).first()

    if existing_attendance:
        raise ValueError(
            "Cannot delete a lecture session with existing attendance records"
        )

    db.delete(lecture_session)
    db.commit()

    return True