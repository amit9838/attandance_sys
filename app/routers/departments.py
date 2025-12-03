from fastapi import APIRouter, HTTPException, status, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from app.models import DepartmentCreate, DepartmentResponse
from app.system.database import db

router = APIRouter(prefix="/api/departments", tags=["departments"])


def get_db() -> AsyncIOMotorDatabase:
    return db


@router.post("", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(dept: DepartmentCreate):
    department = {
        "department_name": dept.department_name,
        "submitted_by": "system",
        "updated_at": datetime.utcnow(),
    }
    result = await db.departments.insert_one(department)
    created_dept = await db.departments.find_one({"_id": result.inserted_id})
    return {**created_dept, "_id": str(created_dept["_id"])}


@router.get("", response_model=list[DepartmentResponse])
async def get_all_departments():
    departments = await db.departments.find().to_list(None)
    return [{**d, "_id": str(d["_id"])} for d in departments]


@router.get("/{dept_id}", response_model=DepartmentResponse)
async def get_department(dept_id: str):
    if not ObjectId.is_valid(dept_id):
        raise HTTPException(status_code=400, detail="Invalid department ID")

    dept = await db.departments.find_one({"_id": ObjectId(dept_id)})
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")

    return {**dept, "_id": str(dept["_id"])}


@router.put("/{dept_id}", response_model=DepartmentResponse)
async def update_department(dept_id: str, dept: DepartmentCreate):
    if not ObjectId.is_valid(dept_id):
        raise HTTPException(status_code=400, detail="Invalid department ID")

    update_data = {
        "department_name": dept.department_name,
        "updated_at": datetime.utcnow(),
    }

    result = await db.departments.update_one(
        {"_id": ObjectId(dept_id)}, {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Department not found")

    updated_dept = await db.departments.find_one({"_id": ObjectId(dept_id)})
    return {**updated_dept, "_id": str(updated_dept["_id"])}


@router.delete("/{dept_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(dept_id: str):
    if not ObjectId.is_valid(dept_id):
        raise HTTPException(status_code=400, detail="Invalid department ID")

    result = await db.departments.delete_one({"_id": ObjectId(dept_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Department not found")

    return None
