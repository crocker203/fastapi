# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", 
             response_model=schemas.User,
             status_code=status.HTTP_201_CREATED,
             summary="Create new user",
             description="Register a new user with email, username and password")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    
    - **email**: must be unique and valid email
    - **username**: must be unique
    - **password**: will be hashed
    """
    # Check if email exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username exists
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    return crud.create_user(db=db, user=user)

@router.get("/", 
            response_model=List[schemas.User],
            summary="Get all users",
            description="Retrieve list of users with pagination")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get users with pagination.
    
    - **skip**: number of records to skip
    - **limit**: maximum number of records to return
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}",
            response_model=schemas.User,
            summary="Get user by ID",
            description="Retrieve user details by user ID")
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by ID.
    
    - **user_id**: ID of the user to retrieve
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user
