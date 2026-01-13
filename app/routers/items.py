# app/routers/items.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db
from app.routers.auth import get_current_user

router = APIRouter(prefix="/items", tags=["items"])

@router.post("/",
             response_model=schemas.Item,
             status_code=status.HTTP_201_CREATED)
def create_item_for_user(
    item: schemas.ItemCreate,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create item for current user.
    Requires authentication.
    """
    return crud.create_user_item(db=db, item=item, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Item])
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all items with pagination.
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
