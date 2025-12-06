from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.session import get_db
from app.models.models import Tutor

router = APIRouter()

@router.get("/", response_model=List[Tutor])
def read_tutors(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    course: Optional[str] = None,
) -> Any:
    query = select(Tutor)
    if course:
        # Simple case-insensitive partial match for MVP
        query = query.where(Tutor.course.contains(course))
    query = query.offset(skip).limit(limit)
    tutors = db.exec(query).all()
    return tutors

@router.get("/{id}", response_model=Tutor)
def read_tutor(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    tutor = db.get(Tutor, id)
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor not found")
    return tutor
