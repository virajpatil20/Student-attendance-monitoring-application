from sqlalchemy.orm import Session
from app.models.course import Course
from app.models.department import Department
from app.schemas.course import CourseCreate, CourseUpdate


def create_course(db: Session, course_data: CourseCreate):
    # Verify department exists
    department = db.query(Department).filter(
        Department.id == course_data.department_id
    ).first()

    if not department:
        raise ValueError("Department does not exist")

    # Check duplicate course code within department
    existing = db.query(Course).filter(
        Course.department_id == course_data.department_id,
        Course.code == course_data.code
    ).first()

    if existing:
        raise ValueError("Course code already exists in this department")

    course = Course(**course_data.model_dump())

    db.add(course)
    db.commit()
    db.refresh(course)

    return course


def get_course(db: Session, course_id: int):
    return db.query(Course).filter(
        Course.id == course_id
    ).first()


def get_all_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Course).offset(skip).limit(limit).all()


def get_courses_by_department(
    db: Session,
    department_id: int,
    skip: int = 0,
    limit: int = 100
):
    return db.query(Course).filter(
        Course.department_id == department_id
    ).offset(skip).limit(limit).all()


def update_course(
    db: Session,
    course_id: int,
    course_data: CourseUpdate
):
    course = get_course(db, course_id)

    if not course:
        return None

    update_data = course_data.model_dump(exclude_unset=True)

    new_department_id = update_data.get(
        "department_id", course.department_id
    )
    new_code = update_data.get("code", course.code)

    department = db.query(Department).filter(
        Department.id == new_department_id
    ).first()

    if not department:
        raise ValueError("Department does not exist")

    duplicate = db.query(Course).filter(
        Course.department_id == new_department_id,
        Course.code == new_code,
        Course.id != course_id
    ).first()

    if duplicate:
        raise ValueError("Course code already exists in this department")

    for key, value in update_data.items():
        setattr(course, key, value)

    db.commit()
    db.refresh(course)

    return course


def delete_course(db: Session, course_id: int):
    course = get_course(db, course_id)

    if not course:
        return None

    db.delete(course)
    db.commit()

    return True