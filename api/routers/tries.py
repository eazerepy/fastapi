from pydantic import BaseModel
from typing import Optional, List
from fastapi import APIRouter, status, HTTPException

from api.models import Try
from api.deps import db_dependency, user_dependency

router = APIRouter(
    prefix='/tries',
    tags=['tries']
)

class TryBase(BaseModel):
    name: str
    description: Optional[str] = None

class TryCreate(TryBase):
    pass

class TryResponse(TryBase):
    id: int

    class Config:
        orm_mode = True

# Change this endpoint to not require try_id
@router.get('/', response_model=List[TryResponse])
def get_tries(db: db_dependency, user: user_dependency):
    return db.query(Try).all()

@router.get('/{try_id}', response_model=TryResponse)
def get_try(db: db_dependency, user: user_dependency, try_id: int):
    db_try = db.query(Try).filter(Try.id == try_id).first()
    if db_try is None:
        raise HTTPException(status_code=404, detail="Try not found")
    return db_try

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TryResponse)
def create_try(db: db_dependency, user: user_dependency, try_: TryCreate):
    db_try = Try(**try_.dict())
    db.add(db_try)
    db.commit()
    db.refresh(db_try)
    return db_try

@router.delete("/{try_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_try(db: db_dependency, user: user_dependency, try_id: int):
    db_try = db.query(Try).filter(Try.id == try_id).first()
    if db_try is None:
        raise HTTPException(status_code=404, detail="Try not found")
    db.delete(db_try)
    db.commit()
    return {"ok": True}

