from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
from datetime import datetime
from bson import ObjectId

# Import routers
from app.routers import courses, students, departments, users, attendance

load_dotenv()



app = FastAPI(
    title="Attendance Management System",
    description="FastAPI + MongoDB",
    version="1.0.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(departments.router)
app.include_router(courses.router)
app.include_router(students.router)
app.include_router(users.router)
app.include_router(attendance.router)



@app.get("/")
async def root():
    return {
        "message": "Attendance Management System API",
        "docs": "http://localhost:8000/docs",
        "health": "http://localhost:8000/health",
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
