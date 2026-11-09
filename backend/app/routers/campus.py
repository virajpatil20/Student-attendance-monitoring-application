from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.campus import CampusCreate, CampusUpdate, CampusResponse
from app.services.campus_service import (
    create_campus,
    get_campus,
    get_all_campuses,
    get_campuses_by_institution,
    update_campus,
    delete_campus
)

router = APIRouter(
    prefix="/campuses",
    tags=["Campuses"]
)


@router.post("/", response_model=CampusResponse, status_code=201)
def create_campus_api(
    campus_data: CampusCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_campus(db, campus_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[CampusResponse])
def get_all_campuses_api(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_all_campuses(db, skip, limit)


@router.get("/institution/{institution_id}", response_model=list[CampusResponse])
def get_campuses_by_institution_api(
    institution_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_campuses_by_institution(
        db, institution_id, skip, limit
    )


@router.get("/{campus_id}", response_model=CampusResponse)
def get_campus_api(
    campus_id: int,
    db: Session = Depends(get_db)
):
    campus = get_campus(db, campus_id)

    if not campus:
        raise HTTPException(status_code=404, detail="Campus not found")

    return campus


@router.put("/{campus_id}", response_model=CampusResponse)
def update_campus_api(
    campus_id: int,
    campus_data: CampusUpdate,
    db: Session = Depends(get_db)
):
    try:
        campus = update_campus(db, campus_id, campus_data)

        if not campus:
            raise HTTPException(status_code=404, detail="Campus not found")

        return campus

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{campus_id}")
def delete_campus_api(
    campus_id: int,
    db: Session = Depends(get_db)
):
    try:
        result = delete_campus(db, campus_id)

        if not result:
            raise HTTPException(status_code=404, detail="Campus not found")

        return {"message": "Campus deleted successfully"}

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))