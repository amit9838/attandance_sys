Attendance Management System – FastAPI + MongoDB

## Features

- FastAPI async backend with MongoDB (Motor driver).
- CRUD APIs for:
  - Department
  - Course
  - Student
  - User (with password hashing)
- Attendance APIs:
  - Mark attendance for a student in a course.
  - Get today’s attendance for a student in a course.
  - Get full attendance history for a student.
  - Get full attendance list for a course.
  - Get attendance statistics for a course (present, absent, percentage).

## Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn
- MongoDB (Motor / PyMongo)
- Pydantic v2

## Project Structure

- main.py – FastAPI app, MongoDB connection, router registration.
- models.py – Pydantic schemas for all entities.
- routers/
  - departments.py – CRUD for departments.
  - courses.py – CRUD for courses.
  - students.py – CRUD for students.
  - users.py – CRUD for users and registration.
  - attendance.py – APIs for marking and checking attendance.
- requirements.txt – Python dependencies.

## Setup Instructions

DB config
- MONGODB_URL=mongodb://localhost:27017
- DATABASE_NAME=attendance_db
- API_PORT=8000

1) Run FastAPI server

- uvicorn main:app --reload --port 8000

Open the interactive API docs at:

- http://localhost:8000/docs

## Core Endpoints

Base URL: http://localhost:8000

Entities:

- Department:
  - POST /api/departments
  - GET /api/departments
  - GET /api/departments/{id}
  - PUT /api/departments/{id}
  - DELETE /api/departments/{id}

- Course:
  - POST /api/courses
  - GET /api/courses
  - GET /api/courses/{id}
  - PUT /api/courses/{id}
  - DELETE /api/courses/{id}

- Student:
  - POST /api/students
  - GET /api/students
  - GET /api/students/{id}
  - PUT /api/students/{id}
  - DELETE /api/students/{id}

- User:
  - POST /api/users/register
  - GET /api/users
  - GET /api/users/{id}
  - PUT /api/users/{id}
  - DELETE /api/users/{id}

Attendance:

- POST /api/attendance
  - Mark attendance for a student in a course (present/absent, once per day).

- GET /api/attendance/{student_id}/{course_id}
  - Get today’s attendance for a student in a course.

- GET /api/attendance/student/{student_id}
  - List all attendance records for a student.

- GET /api/attendance/course/{course_id}
  - List all attendance records for a course.

- GET /api/attendance/stats/{course_id}
  - Get attendance statistics (total records, present, absent, percentage).

- PUT /api/attendance/{attendance_id}
  - Update an existing attendance record.

- DELETE /api/attendance/{attendance_id}
  - Delete an attendance record.

| Method | Endpoint                                 | Purpose                            |
| ------ | ---------------------------------------- | ---------------------------------- |
| POST   | /api/attendance                          | Mark attendance for student        |
| GET    | /api/attendance/{student_id}/{course_id} | Get today's attendance             |
| GET    | /api/attendance/student/{student_id}     | Get all student attendance records |
| GET    | /api/attendance/course/{course_id}       | Get all course attendance records  |
| GET    | /api/attendance/stats/{course_id}        | Get attendance statistics          |
| PUT    | /api/attendance/{attendance_id}          | Update attendance                  |
| DELETE | /api/attendance/{attendance_id}          | Delete attendance                  |

### Docs Screenshot
![alt text](https://github.com/amit9838/attandance_sys/blob/a528b1996d2b4a7a44bd082100fbcfb9aa4569b5/docs.png)