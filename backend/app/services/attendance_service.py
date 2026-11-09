from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from app.models.student import Student
from app.models.course import Course
from app.models.faculty import Faculty
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate


def create_attendance(db: Session, attendance_data: AttendanceCreate):
    # Verify student exists
    student = db.query(Student).filter(
        Student.id == attendance_data.student_id
    ).first()

    if not student:
        raise ValueError("Student does not exist")

    # Verify course exists and belongs to student's department
    course = db.query(Course).filter(
        Course.id == attendance_data.course_id,
        Course.department_id == student.department_id
    ).first()

    if not course:
        raise ValueError("Course does not belong to student's department")

    # Verify faculty if provided
    if attendance_data.faculty_id is not None:
        faculty = db.query(Faculty).filter(
            Faculty.id == attendance_data.faculty_id
        ).first()

        if not faculty:
            raise ValueError("Faculty does not exist")

    # Prevent duplicate attendance for the same student, course and date
    existing = db.query(Attendance).filter(
        Attendance.student_id == attendance_data.student_id,
        Attendance.course_id == attendance_data.course_id,
        Attendance.attendance_date == attendance_data.attendance_date
    ).first()

    if existing:
        raise ValueError(
            "Attendance already marked for this student, course and date"
        )

    attendance = Attendance(**attendance_data.model_dump())

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return attendance


def get_attendance(db: Session, attendance_id: int):
    return db.query(Attendance).filter(
        Attendance.id == attendance_id
    ).first()


def get_all_attendance(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Attendance).offset(skip).limit(limit).all()


def get_attendance_by_student(
    db: Session,
    student_id: int,
    skip: int = 0,
    limit: int = 100
):
    return db.query(Attendance).filter(
        Attendance.student_id == student_id
    ).order_by(
        Attendance.attendance_date.desc()
    ).offset(skip).limit(limit).all()


def get_attendance_by_course(
    db: Session,
    course_id: int,
    skip: int = 0,
    limit: int = 100
):
    return db.query(Attendance).filter(
        Attendance.course_id == course_id
    ).order_by(
        Attendance.attendance_date.desc()
    ).offset(skip).limit(limit).all()


def get_attendance_by_date(db: Session, attendance_date):
    return db.query(Attendance).filter(
        Attendance.attendance_date == attendance_date
    ).all()


def update_attendance(
    db: Session,
    attendance_id: int,
    attendance_data: AttendanceUpdate
):
    attendance = get_attendance(db, attendance_id)

    if not attendance:
        return None

    update_data = attendance_data.model_dump(exclude_unset=True)

    new_student_id = update_data.get(
        "student_id", attendance.student_id
    )
    new_course_id = update_data.get(
        "course_id", attendance.course_id
    )
    new_date = update_data.get(
        "attendance_date", attendance.attendance_date
    )

    student = db.query(Student).filter(
        Student.id == new_student_id
    ).first()

    if not student:
        raise ValueError("Student does not exist")

    course = db.query(Course).filter(
        Course.id == new_course_id,
        Course.department_id == student.department_id
    ).first()

    if not course:
        raise ValueError("Course does not belong to student's department")

    # Check for duplicate attendance
    duplicate = db.query(Attendance).filter(
        Attendance.student_id == new_student_id,
        Attendance.course_id == new_course_id,
        Attendance.attendance_date == new_date,
        Attendance.id != attendance_id
    ).first()

    if duplicate:
        raise ValueError(
            "Attendance already exists for this student, course and date"
        )

    # Validate faculty if changed
    if "faculty_id" in update_data and update_data["faculty_id"] is not None:
        faculty = db.query(Faculty).filter(
            Faculty.id == update_data["faculty_id"]
        ).first()

        if not faculty:
            raise ValueError("Faculty does not exist")

    for key, value in update_data.items():
        setattr(attendance, key, value)

    db.commit()
    db.refresh(attendance)

    return attendance


def delete_attendance(db: Session, attendance_id: int):
    attendance = get_attendance(db, attendance_id)

    if not attendance:
        return None

    db.delete(attendance)
    db.commit()

    return True