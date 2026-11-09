from sqlalchemy.orm import Session
from app.models.campus import Campus
from app.schemas.campus import CampusCreate, CampusUpdate


def create_campus(db: Session, campus_data: CampusCreate):
    # Verify that the institution exists
    from app.models.institution import Institution

    institution = db.query(Institution).filter(
        Institution.id == campus_data.institution_id
    ).first()

    if not institution:
        raise ValueError("Institution does not exist")

    # Check duplicate campus code within the institution
    existing = db.query(Campus).filter(
        Campus.institution_id == campus_data.institution_id,
        Campus.code == campus_data.code
    ).first()

    if existing:
        raise ValueError("Campus code already exists in this institution")

    campus = Campus(**campus_data.model_dump())

    db.add(campus)
    db.commit()
    db.refresh(campus)

    return campus


def get_campus(db: Session, campus_id: int):
    return db.query(Campus).filter(
        Campus.id == campus_id
    ).first()


def get_all_campuses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Campus).offset(skip).limit(limit).all()


def get_campuses_by_institution(
    db: Session,
    institution_id: int,
    skip: int = 0,
    limit: int = 100
):
    return db.query(Campus).filter(
        Campus.institution_id == institution_id
    ).offset(skip).limit(limit).all()


def update_campus(
    db: Session,
    campus_id: int,
    campus_data: CampusUpdate
):
    campus = get_campus(db, campus_id)

    if not campus:
        return None

    update_data = campus_data.model_dump(exclude_unset=True)

    new_institution_id = update_data.get(
        "institution_id", campus.institution_id
    )
    new_code = update_data.get("code", campus.code)

    from app.models.institution import Institution

    institution = db.query(Institution).filter(
        Institution.id == new_institution_id
    ).first()

    if not institution:
        raise ValueError("Institution does not exist")

    duplicate = db.query(Campus).filter(
        Campus.institution_id == new_institution_id,
        Campus.code == new_code,
        Campus.id != campus_id
    ).first()

    if duplicate:
        raise ValueError("Campus code already exists in this institution")

    for key, value in update_data.items():
        setattr(campus, key, value)

    db.commit()
    db.refresh(campus)

    return campus


def delete_campus(db: Session, campus_id: int):
    campus = get_campus(db, campus_id)

    if not campus:
        return None

    db.delete(campus)
    db.commit()

    return True