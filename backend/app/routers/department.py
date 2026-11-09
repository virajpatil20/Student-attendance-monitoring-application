from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse
)
from app.services.department_service import (
    create_department,
    get_department,
    get_all_departments,
    get_departments_by_campus,
    update_department,
    delete_department
)

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.post("/", response_model=DepartmentResponse, status_code=201)
def create_department_api(
    department_data: DepartmentCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_department(db, department_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[DepartmentResponse])
def get_all_departments_api(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_all_departments(db, skip, limit)


@router.get("/campus/{campus_id}", response_model=list[DepartmentResponse])
def get_departments_by_campus_api(
    campus_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_departments_by_campus(db, campus_id, skip, limit)


@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department_api(
    department_id: int,
    db: Session = Depends(get_db)
):
    department = get_department(db, department_id)

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    return department


@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department_api(
    department_id: int,
    department_data: DepartmentUpdate,
    db: Session = Depends(get_db)
):
    try:
        department = update_department(
            db, department_id, department_data
        )

        if not department:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

        return department

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{department_id}")
def delete_department_api(
    department_id: int,
    db: Session = Depends(get_db)
):
    try:
        result = delete_department(db, department_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

        return {"message": "Department deleted successfully"}

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))