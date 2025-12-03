from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# Department Models
class DepartmentCreate(BaseModel):
    department_name: str


class DepartmentResponse(BaseModel):
    id: str = Field(alias="_id")
    department_name: str
    submitted_by: Optional[str] = None
    updated_at: Optional[datetime] = None

    class Config:
        populate_by_name = True


# Course Models
class CourseCreate(BaseModel):
    course_name: str
    department_id: str
    semester: int = Field(ge=1, le=8)
    class_: str = Field(alias="class")
    lecture_hours: int = Field(ge=0)


class CourseResponse(BaseModel):
    id: str = Field(alias="_id")
    course_name: str
    department_id: str
    semester: int
    class_: str = Field(alias="class")
    lecture_hours: int
    submitted_by: Optional[str] = None
    updated_at: Optional[datetime] = None

    class Config:
        populate_by_name = True


# Student Models
class StudentCreate(BaseModel):
    full_name: str
    department_id: str
    class_: str = Field(alias="class")


class StudentResponse(BaseModel):
    id: str = Field(alias="_id")
    full_name: str
    department_id: str
    class_: str = Field(alias="class")
    submitted_by: Optional[str] = None
    updated_at: Optional[datetime] = None

    class Config:
        populate_by_name = True


# User Models
class UserCreate(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str
    type: str = Field(pattern="^(admin|faculty|student)$")


class UserResponse(BaseModel):
    id: str = Field(alias="_id")
    full_name: str
    username: str
    email: str
    type: str
    submitted_by: Optional[str] = None
    updated_at: Optional[datetime] = None

    class Config:
        populate_by_name = True


class UserLogin(BaseModel):
    username: str
    password: str


# Attendance Models
class AttendanceCreate(BaseModel):
    student_id: str
    course_id: str
    present: bool


class AttendanceResponse(BaseModel):
    id: str = Field(alias="_id")
    student_id: str
    course_id: str
    present: bool
    submitted_by: Optional[str] = None
    updated_at: Optional[datetime] = None

    class Config:
        populate_by_name = True
