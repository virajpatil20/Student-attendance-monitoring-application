from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.institution import (
    InstitutionCreate,
    InstitutionUpdate,
    InstitutionResponse
)
from app.services.institution_service import (
    create_institution,
    get_institution,
    get_all_institutions,
    update_institution,
    delete_institution
)

router = APIRouter(
    prefix="/institutions",
    tags=["Institutions"]
)


@router.post("/", response_model=InstitutionResponse, status_code=201)
def create_institution_api(
    institution_data: InstitutionCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_institution(db, institution_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[InstitutionResponse])
def get_all_institutions_api(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_all_institutions(db, skip, limit)


@router.get("/{institution_id}", response_model=InstitutionResponse)
def get_institution_api(
    institution_id: int,
    db: Session = Depends(get_db)
):
    institution = get_institution(db, institution_id)

    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")

    return institution


@router.put("/{institution_id}", response_model=InstitutionResponse)
def update_institution_api(
    institution_id: int,
    institution_data: InstitutionUpdate,
    db: Session = Depends(get_db)
):
    try:
        institution = update_institution(
            db, institution_id, institution_data
        )

        if not institution:
            raise HTTPException(
                status_code=404,
                detail="Institution not found"
            )

        return institution

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{institution_id}")
def delete_institution_api(
    institution_id: int,
    db: Session = Depends(get_db)
):
    try:
        result = delete_institution(db, institution_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Institution not found"
            )

        return {"message": "Institution deleted successfully"}

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))