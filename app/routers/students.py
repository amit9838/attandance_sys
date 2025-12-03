from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from datetime import datetime
from app.models import StudentCreate, StudentResponse
from app.system.database import db

router = APIRouter(prefix="/api/students", tags=["students"])


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(student: StudentCreate):
    # Verify department exists
    dept = await db.departments.find_one({"_id": ObjectId(student.department_id)})
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")

    student_doc = {
        "full_name": student.full_name,
        "department_id": student.department_id,
        "class": student.class_,
        "submitted_by": "system",
        "updated_at": datetime.utcnow(),
    }

    result = await db.students.insert_one(student_doc)
    created = await db.students.find_one({"_id": result.inserted_id})
    return {**created, "_id": str(created["_id"])}


@router.get("", response_model=list[StudentResponse])
async def get_all_students():
    students = await db.students.find().to_list(None)
    return [{**s, "_id": str(s["_id"])} for s in students]


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id: str):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=400, detail="Invalid student ID")

    student = await db.students.find_one({"_id": ObjectId(student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return {**student, "_id": str(student["_id"])}


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(student_id: str, student: StudentCreate):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=400, detail="Invalid student ID")

    dept = await db.departments.find_one({"_id": ObjectId(student.department_id)})
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")

    update_data = {
        "full_name": student.full_name,
        "department_id": student.department_id,
        "class": student.class_,
        "updated_at": datetime.utcnow(),
    }

    result = await db.students.update_one(
        {"_id": ObjectId(student_id)}, {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    updated = await db.students.find_one({"_id": ObjectId(student_id)})
    return {**updated, "_id": str(updated["_id"])}


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: str):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=400, detail="Invalid student ID")

    result = await db.students.delete_one({"_id": ObjectId(student_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
