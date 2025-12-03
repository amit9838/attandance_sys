from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from datetime import datetime
from app.models import CourseCreate, CourseResponse
from app.system.database import db

router = APIRouter(prefix="/api/courses", tags=["courses"])


@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseCreate):
    # Verify department exists
    dept = await db.departments.find_one({"_id": ObjectId(course.department_id)})
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")

    course_doc = {
        "course_name": course.course_name,
        "department_id": course.department_id,
        "semester": course.semester,
        "class": course.class_,
        "lecture_hours": course.lecture_hours,
        "submitted_by": "system",
        "updated_at": datetime.utcnow(),
    }

    result = await db.courses.insert_one(course_doc)
    created = await db.courses.find_one({"_id": result.inserted_id})
    return {**created, "_id": str(created["_id"])}


@router.get("", response_model=list[CourseResponse])
async def get_all_courses():
    courses = await db.courses.find().to_list(None)
    return [{**c, "_id": str(c["_id"])} for c in courses]


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: str):
    if not ObjectId.is_valid(course_id):
        raise HTTPException(status_code=400, detail="Invalid course ID")

    course = await db.courses.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return {**course, "_id": str(course["_id"])}


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(course_id: str, course: CourseCreate):
    if not ObjectId.is_valid(course_id):
        raise HTTPException(status_code=400, detail="Invalid course ID")

    dept = await db.departments.find_one({"_id": ObjectId(course.department_id)})
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")

    update_data = {
        "course_name": course.course_name,
        "department_id": course.department_id,
        "semester": course.semester,
        "class": course.class_,
        "lecture_hours": course.lecture_hours,
        "updated_at": datetime.utcnow(),
    }

    result = await db.courses.update_one(
        {"_id": ObjectId(course_id)}, {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Course not found")

    updated = await db.courses.find_one({"_id": ObjectId(course_id)})
    return {**updated, "_id": str(updated["_id"])}


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: str):
    if not ObjectId.is_valid(course_id):
        raise HTTPException(status_code=400, detail="Invalid course ID")

    result = await db.courses.delete_one({"_id": ObjectId(course_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Course not found")
