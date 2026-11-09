from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.admin import (
    AdminCreate,
    AdminUpdate,
    AdminResponse
)

from app.services.admin_service import (
    create_admin,
    get_admin,
    get_admin_by_email,
    get_all_admins,
    update_admin,
    delete_admin
)

router = APIRouter(
    prefix="/admins",
    tags=["Admins"]
)


@router.post("/", response_model=AdminResponse, status_code=201)
def create_admin_api(
    admin_data: AdminCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_admin(db, admin_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[AdminResponse])
def get_all_admins_api(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_all_admins(db, skip, limit)


@router.get("/email/{email}", response_model=AdminResponse)
def get_admin_by_email_api(
    email: str,
    db: Session = Depends(get_db)
):
    admin = get_admin_by_email(db, email)

    if not admin:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )

    return admin


@router.get("/{admin_id}", response_model=AdminResponse)
def get_admin_api(
    admin_id: int,
    db: Session = Depends(get_db)
):
    admin = get_admin(db, admin_id)

    if not admin:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )

    return admin


@router.put("/{admin_id}", response_model=AdminResponse)
def update_admin_api(
    admin_id: int,
    admin_data: AdminUpdate,
    db: Session = Depends(get_db)
):
    try:
        admin = update_admin(db, admin_id, admin_data)

        if not admin:
            raise HTTPException(
                status_code=404,
                detail="Admin not found"
            )

        return admin

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{admin_id}")
def delete_admin_api(
    admin_id: int,
    db: Session = Depends(get_db)
):
    try:
        result = delete_admin(db, admin_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Admin not found"
            )

        return {"message": "Admin deleted successfully"}

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))