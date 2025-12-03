from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from datetime import datetime
from app.models import UserCreate, UserResponse
from app.system.database import db
import hashlib

router = APIRouter(prefix="/api/users", tags=["users"])


def hash_password(password: str) -> str:
    """Simple password hashing (use bcrypt in production)"""
    return hashlib.sha256(password.encode()).hexdigest()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(user: UserCreate):
    # Check if username exists
    existing = await db.users.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Check if email exists
    existing_email = await db.users.find_one({"email": user.email})
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_doc = {
        "full_name": user.full_name,
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
        "type": user.type,
        "submitted_by": "system",
        "updated_at": datetime.utcnow(),
    }

    result = await db.users.insert_one(user_doc)
    created = await db.users.find_one({"_id": result.inserted_id})

    # Don't return password in response
    created.pop("password", None)
    return {**created, "_id": str(created["_id"])}


@router.get("", response_model=list[UserResponse])
async def get_all_users():
    users = await db.users.find().to_list(None)
    result = []
    for u in users:
        u.pop("password", None)
        result.append({**u, "_id": str(u["_id"])})
    return result


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.pop("password", None)
    return {**user, "_id": str(user["_id"])}


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user: UserCreate):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    # Check username uniqueness (excluding current user)
    existing = await db.users.find_one(
        {"username": user.username, "_id": {"$ne": ObjectId(user_id)}}
    )
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    update_data = {
        "full_name": user.full_name,
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
        "type": user.type,
        "updated_at": datetime.utcnow(),
    }

    result = await db.users.update_one(
        {"_id": ObjectId(user_id)}, {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    updated = await db.users.find_one({"_id": ObjectId(user_id)})
    updated.pop("password", None)
    return {**updated, "_id": str(updated["_id"])}


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    result = await db.users.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
