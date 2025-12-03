Attendance Management System – FastAPI + MongoDB

This project is a simple attendance management backend built with FastAPI and MongoDB. It supports CRUD operations for departments, courses, students, users, and provides APIs for marking and viewing attendance records.

## Features

- FastAPI async backend with MongoDB (Motor driver).
- CRUD APIs for:
  - Department
  - Course
  - Student
  - User (with basic password hashing)
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
- Docker (for running MongoDB locally)

## Project Structure

- main.py – FastAPI app, MongoDB connection, router registration.
- models.py – Pydantic schemas for all entities.
- routers/
  - departments.py – CRUD for departments.
  - courses.py – CRUD for courses.
  - students.py – CRUD for students.
  - users.py – CRUD for users and registration.
  - attendance.py – APIs for marking and checking attendance.
- .env – Environment variables (MongoDB URL, DB name, port).
- requirements.txt – Python dependencies.

## Setup Instructions

1) Clone and create environment

- Clone the repository (or copy the code files into a folder).
- Create and activate a virtual environment.

Example:

- python -m venv venv
- source venv/bin/activate  (Linux/macOS)
- venv\Scripts\activate     (Windows)

2) Install dependencies

- pip install -r requirements.txt

3) Run MongoDB (using Docker)

- docker run -d -p 27017:27017 --name mongodb mongo:latest

4) Configure environment

Create a .env file in the project root:

- MONGODB_URL=mongodb://localhost:27017
- DATABASE_NAME=attendance_db
- API_PORT=8000

5) Run FastAPI server

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

## Example Requests

1) Create Department

- POST /api/departments
- Body:
  - {
      "department_name": "Computer Science"
    }

2) Create Course

- POST /api/courses
- Body:
  - {
      "course_name": "Python 101",
      "department_id": "<department_object_id>",
      "semester": 1,
      "class": "B1",
      "lecture_hours": 40
    }

3) Add Student

- POST /api/students
- Body:
  - {
      "full_name": "John Doe",
      "department_id": "<department_object_id>",
      "class": "B1"
    }

4) Register User

- POST /api/users/register
- Body:
  - {
      "full_name": "Jane Smith",
      "username": "jane_smith",
      "email": "jane@example.com",
      "password": "secret",
      "type": "admin"
    }

5) Mark Attendance

- POST /api/attendance
- Body:
  - {
      "student_id": "<student_object_id>",
      "course_id": "<course_object_id>",
      "present": true
    }

6) Get Course Attendance Stats

- GET /api/attendance/stats/<course_object_id>


### Docs Screenshot
![alt text](https://github.com/amit9838/attandance_sys/blob/a528b1996d2b4a7a44bd082100fbcfb9aa4569b5/docs.png)