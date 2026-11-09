from sqlalchemy.orm import Session
from app.models.faculty import Faculty
from app.models.department import Department
from app.schemas.faculty import FacultyCreate, FacultyUpdate


def create_faculty(db: Session, faculty_data: FacultyCreate):
    # Verify department exists
    department = db.query(Department).filter(
        Department.id == faculty_data.department_id
    ).first()

    if not department:
        raise ValueError("Department does not exist")

    # Check duplicate employee code within department
    existing = db.query(Faculty).filter(
        Faculty.department_id == faculty_data.department_id,
        Faculty.employee_code == faculty_data.employee_code
    ).first()

    if existing:
        raise ValueError("Employee code already exists in this department")

    # Check email uniqueness
    existing_email = db.query(Faculty).filter(
        Faculty.email == faculty_data.email
    ).first()

    if existing_email:
        raise ValueError("Faculty email already exists")

    faculty = Faculty(**faculty_data.model_dump())

    db.add(faculty)
    db.commit()
    db.refresh(faculty)

    return faculty


def get_faculty(db: Session, faculty_id: int):
    return db.query(Faculty).filter(
        Faculty.id == faculty_id
    ).first()


def get_all_faculty(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Faculty).offset(skip).limit(limit).all()


def get_faculty_by_department(
    db: Session,
    department_id: int,
    skip: int = 0,
    limit: int = 100
):
    return db.query(Faculty).filter(
        Faculty.department_id == department_id
    ).offset(skip).limit(limit).all()


def update_faculty(
    db: Session,
    faculty_id: int,
    faculty_data: FacultyUpdate
):
    faculty = get_faculty(db, faculty_id)

    if not faculty:
        return None

    update_data = faculty_data.model_dump(exclude_unset=True)

    new_department_id = update_data.get(
        "department_id", faculty.department_id
    )
    new_employee_code = update_data.get(
        "employee_code", faculty.employee_code
    )
    new_email = update_data.get("email", faculty.email)

    department = db.query(Department).filter(
        Department.id == new_department_id
    ).first()

    if not department:
        raise ValueError("Department does not exist")

    duplicate_code = db.query(Faculty).filter(
        Faculty.department_id == new_department_id,
        Faculty.employee_code == new_employee_code,
        Faculty.id != faculty_id
    ).first()

    if duplicate_code:
        raise ValueError("Employee code already exists in this department")

    duplicate_email = db.query(Faculty).filter(
        Faculty.email == new_email,
        Faculty.id != faculty_id
    ).first()

    if duplicate_email:
        raise ValueError("Faculty email already exists")

    for key, value in update_data.items():
        setattr(faculty, key, value)

    db.commit()
    db.refresh(faculty)

    return faculty


def delete_faculty(db: Session, faculty_id: int):
    faculty = get_faculty(db, faculty_id)

    if not faculty:
        return None

    db.delete(faculty)
    db.commit()

    return True
