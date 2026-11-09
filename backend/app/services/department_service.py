from sqlalchemy.orm import Session
from app.models.department import Department
from app.models.campus import Campus
from app.schemas.department import DepartmentCreate, DepartmentUpdate


def create_department(db: Session, department_data: DepartmentCreate):
    # Verify campus exists
    campus = db.query(Campus).filter(
        Campus.id == department_data.campus_id
    ).first()

    if not campus:
        raise ValueError("Campus does not exist")

    # Check duplicate department code within campus
    existing = db.query(Department).filter(
        Department.campus_id == department_data.campus_id,
        Department.code == department_data.code
    ).first()

    if existing:
        raise ValueError("Department code already exists in this campus")

    department = Department(**department_data.model_dump())

    db.add(department)
    db.commit()
    db.refresh(department)

    return department


def get_department(db: Session, department_id: int):
    return db.query(Department).filter(
        Department.id == department_id
    ).first()


def get_all_departments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Department).offset(skip).limit(limit).all()


def get_departments_by_campus(
    db: Session,
    campus_id: int,
    skip: int = 0,
    limit: int = 100
):
    return db.query(Department).filter(
        Department.campus_id == campus_id
    ).offset(skip).limit(limit).all()


def update_department(
    db: Session,
    department_id: int,
    department_data: DepartmentUpdate
):
    department = get_department(db, department_id)

    if not department:
        return None

    update_data = department_data.model_dump(exclude_unset=True)

    new_campus_id = update_data.get(
        "campus_id", department.campus_id
    )
    new_code = update_data.get("code", department.code)

    campus = db.query(Campus).filter(
        Campus.id == new_campus_id
    ).first()

    if not campus:
        raise ValueError("Campus does not exist")

    duplicate = db.query(Department).filter(
        Department.campus_id == new_campus_id,
        Department.code == new_code,
        Department.id != department_id
    ).first()

    if duplicate:
        raise ValueError("Department code already exists in this campus")

    for key, value in update_data.items():
        setattr(department, key, value)

    db.commit()
    db.refresh(department)

    return department


def delete_department(db: Session, department_id: int):
    department = get_department(db, department_id)

    if not department:
        return None

    db.delete(department)
    db.commit()

    return True