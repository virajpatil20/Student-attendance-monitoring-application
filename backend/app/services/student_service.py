from sqlalchemy.orm import Session
from app.models.student import Student
from app.models.department import Department
from app.models.course import Course
from app.schemas.student import StudentCreate, StudentUpdate


def create_student(db: Session, student_data: StudentCreate):
    # Verify department exists
    department = db.query(Department).filter(
        Department.id == student_data.department_id
    ).first()

    if not department:
        raise ValueError("Department does not exist")

    # Verify course exists and belongs to the selected department
    course = db.query(Course).filter(
        Course.id == student_data.course_id,
        Course.department_id == student_data.department_id
    ).first()

    if not course:
        raise ValueError("Course does not belong to the selected department")

    # Check enrollment number uniqueness
    existing = db.query(Student).filter(
        Student.enrollment_number == student_data.enrollment_number
    ).first()

    if existing:
        raise ValueError("Enrollment number already exists")

    # Check email uniqueness if provided
    if student_data.email:
        existing_email = db.query(Student).filter(
            Student.email == student_data.email
        ).first()

        if existing_email:
            raise ValueError("Student email already exists")

    student = Student(**student_data.model_dump())

    db.add(student)
    db.commit()
    db.refresh(student)

    return student


def get_student(db: Session, student_id: int):
    return db.query(Student).filter(
        Student.id == student_id
    ).first()


def get_student_by_enrollment(db: Session, enrollment_number: str):
    return db.query(Student).filter(
        Student.enrollment_number == enrollment_number
    ).first()


def get_all_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Student).offset(skip).limit(limit).all()


def get_students_by_department(
    db: Session,
    department_id: int,
    skip: int = 0,
    limit: int = 100
):
    return db.query(Student).filter(
        Student.department_id == department_id
    ).offset(skip).limit(limit).all()


def update_student(
    db: Session,
    student_id: int,
    student_data: StudentUpdate
):
    student = get_student(db, student_id)

    if not student:
        return None

    update_data = student_data.model_dump(exclude_unset=True)

    new_department_id = update_data.get(
        "department_id", student.department_id
    )
    new_course_id = update_data.get(
        "course_id", student.course_id
    )

    # Validate department
    department = db.query(Department).filter(
        Department.id == new_department_id
    ).first()

    if not department:
        raise ValueError("Department does not exist")

    # Validate course-department relationship
    course = db.query(Course).filter(
        Course.id == new_course_id,
        Course.department_id == new_department_id
    ).first()

    if not course:
        raise ValueError("Course does not belong to the selected department")

    # Check enrollment number uniqueness
    new_enrollment = update_data.get(
        "enrollment_number", student.enrollment_number
    )

    duplicate_enrollment = db.query(Student).filter(
        Student.enrollment_number == new_enrollment,
        Student.id != student_id
    ).first()

    if duplicate_enrollment:
        raise ValueError("Enrollment number already exists")

    # Check email uniqueness
    if "email" in update_data and update_data["email"]:
        duplicate_email = db.query(Student).filter(
            Student.email == update_data["email"],
            Student.id != student_id
        ).first()

        if duplicate_email:
            raise ValueError("Student email already exists")

    for key, value in update_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return student


def delete_student(db: Session, student_id: int):
    student = get_student(db, student_id)

    if not student:
        return None

    db.delete(student)
    db.commit()

    return True