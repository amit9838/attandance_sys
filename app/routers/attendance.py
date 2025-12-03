from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from datetime import datetime
from app.models import AttendanceCreate, AttendanceResponse
from app.system.database import db
import time

router = APIRouter(prefix="/api/attendance", tags=["attendance"])


@router.post("", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
async def mark_attendance(attendance: AttendanceCreate):
    """Mark attendance for a student in a course"""

    # Verify student exists
    student = await db.students.find_one({"_id": ObjectId(attendance.student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Verify course exists
    course = await db.courses.find_one({"_id": ObjectId(attendance.course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check if attendance already marked today
    today = int(time.time())
    existing = await db.attendance_log.find_one(
        {
            "student_id": attendance.student_id,
            "course_id": attendance.course_id,
            "date": today,
        }
    )

    if existing:
        raise HTTPException(
            status_code=400, detail="Attendance already marked for this student today"
        )

    attendance_doc = {
        "student_id": attendance.student_id,
        "course_id": attendance.course_id,
        "present": attendance.present,
        "date": today,
        "submitted_by": "system",
        "updated_at": datetime.utcnow(),
    }

    result = await db.attendance_log.insert_one(attendance_doc)
    created = await db.attendance_log.find_one({"_id": result.inserted_id})

    return {**created, "_id": str(created["_id"])}


@router.get("/student/{student_id}", response_model=list[AttendanceResponse])
async def get_student_attendance(student_id: str):
    """Get all attendance records for a student"""

    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=400, detail="Invalid student ID")

    # Verify student exists
    student = await db.students.find_one({"_id": ObjectId(student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    records = await db.attendance_log.find({"student_id": student_id}).to_list(None)
    return [{**r, "_id": str(r["_id"])} for r in records]


@router.get("/course/{course_id}", response_model=list[AttendanceResponse])
async def get_course_attendance(course_id: str):
    """Get all attendance records for a course"""

    if not ObjectId.is_valid(course_id):
        raise HTTPException(status_code=400, detail="Invalid course ID")

    # Verify course exists
    course = await db.courses.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    records = await db.attendance_log.find({"course_id": course_id}).to_list(None)
    return [{**r, "_id": str(r["_id"])} for r in records]


@router.get("/stats/{course_id}")
async def get_attendance_stats(course_id: str):
    """Get attendance statistics for a course"""

    if not ObjectId.is_valid(course_id):
        raise HTTPException(status_code=400, detail="Invalid course ID")

    course = await db.courses.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Get all attendance records
    records = await db.attendance_log.find({"course_id": course_id}).to_list(None)

    if not records:
        return {
            "course_id": course_id,
            "total_records": 0,
            "present": 0,
            "absent": 0,
            "attendance_percentage": 0,
        }

    present_count = sum(1 for r in records if r["present"])
    absent_count = len(records) - present_count
    attendance_percentage = (present_count / len(records)) * 100 if records else 0

    return {
        "course_id": course_id,
        "total_records": len(records),
        "present": present_count,
        "absent": absent_count,
        "attendance_percentage": round(attendance_percentage, 2),
    }


@router.put("/{attendance_id}", response_model=AttendanceResponse)
async def update_attendance(attendance_id: str, attendance: AttendanceCreate):
    """Update attendance record"""

    if not ObjectId.is_valid(attendance_id):
        raise HTTPException(status_code=400, detail="Invalid attendance ID")

    # Verify student and course exist
    student = await db.students.find_one({"_id": ObjectId(attendance.student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    course = await db.courses.find_one({"_id": ObjectId(attendance.course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    update_data = {
        "student_id": attendance.student_id,
        "course_id": attendance.course_id,
        "present": attendance.present,
        "updated_at": datetime.utcnow(),
    }

    result = await db.attendance_log.update_one(
        {"_id": ObjectId(attendance_id)}, {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Attendance record not found")

    updated = await db.attendance_log.find_one({"_id": ObjectId(attendance_id)})
    return {**updated, "_id": str(updated["_id"])}


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attendance(attendance_id: str):
    """Delete attendance record"""

    if not ObjectId.is_valid(attendance_id):
        raise HTTPException(status_code=400, detail="Invalid attendance ID")

    result = await db.attendance_log.delete_one({"_id": ObjectId(attendance_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Attendance record not found")
