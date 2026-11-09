from sqlalchemy.orm import Session
from app.models.institution import Institution
from app.schemas.institution import InstitutionCreate, InstitutionUpdate


def create_institution(db: Session, institution_data: InstitutionCreate):
    existing = db.query(Institution).filter(
        (Institution.name == institution_data.name) |
        (Institution.code == institution_data.code)
    ).first()

    if existing:
        raise ValueError("Institution name or code already exists")

    institution = Institution(**institution_data.model_dump())

    db.add(institution)
    db.commit()
    db.refresh(institution)

    return institution


def get_institution(db: Session, institution_id: int):
    return db.query(Institution).filter(
        Institution.id == institution_id
    ).first()


def get_all_institutions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Institution).offset(skip).limit(limit).all()


def update_institution(
    db: Session,
    institution_id: int,
    institution_data: InstitutionUpdate
):
    institution = get_institution(db, institution_id)

    if not institution:
        return None

    update_data = institution_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(institution, key, value)

    db.commit()
    db.refresh(institution)

    return institution


def delete_institution(db: Session, institution_id: int):
    institution = get_institution(db, institution_id)

    if not institution:
        return None

    db.delete(institution)
    db.commit()

    return True