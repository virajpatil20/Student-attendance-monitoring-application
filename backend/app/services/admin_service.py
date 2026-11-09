from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminUpdate

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_admin(db: Session, admin_data: AdminCreate):
    existing = db.query(Admin).filter(
        Admin.email == admin_data.email
    ).first()

    if existing:
        raise ValueError("Admin email already exists")

    admin_values = admin_data.model_dump()
    password = admin_values.pop("password")
    admin_values["password_hash"] = hash_password(password)

    admin = Admin(**admin_values)

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return admin


def get_admin(db: Session, admin_id: int):
    return db.query(Admin).filter(Admin.id == admin_id).first()


def get_admin_by_email(db: Session, email: str):
    return db.query(Admin).filter(Admin.email == email).first()


def get_all_admins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Admin).offset(skip).limit(limit).all()


def update_admin(db: Session, admin_id: int, admin_data: AdminUpdate):
    admin = get_admin(db, admin_id)

    if not admin:
        return None

    update_data = admin_data.model_dump(exclude_unset=True)

    if "email" in update_data:
        duplicate = db.query(Admin).filter(
            Admin.email == update_data["email"],
            Admin.id != admin_id
        ).first()

        if duplicate:
            raise ValueError("Admin email already exists")

    if update_data.get("password"):
        password = update_data.pop("password")
        update_data["password_hash"] = hash_password(password)
    else:
        update_data.pop("password", None)

    for key, value in update_data.items():
        setattr(admin, key, value)

    db.commit()
    db.refresh(admin)

    return admin


def delete_admin(db: Session, admin_id: int):
    admin = get_admin(db, admin_id)

    if not admin:
        return None

    db.delete(admin)
    db.commit()

    return True