from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api import deps
from app.db.session import get_db
from app.models.models import Opportunity, OpportunityCategory, Bookmark, User

router = APIRouter()

@router.get("/", response_model=List[Opportunity])
def read_opportunities(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category: Optional[OpportunityCategory] = None,
) -> Any:
    query = select(Opportunity)
    if category:
        query = query.where(Opportunity.category == category)
    query = query.offset(skip).limit(limit)
    opportunities = db.exec(query).all()
    return opportunities

@router.get("/{id}", response_model=Opportunity)
def read_opportunity(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    opportunity = db.get(Opportunity, id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opportunity

@router.post("/{id}/bookmark", response_model=Bookmark)
def bookmark_opportunity(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    opportunity = db.get(Opportunity, id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    
    # Check if already bookmarked
    statement = select(Bookmark).where(
        Bookmark.user_id == current_user.id,
        Bookmark.opportunity_id == id
    )
    existing_bookmark = db.exec(statement).first()
    if existing_bookmark:
        return existing_bookmark
        
    bookmark = Bookmark(user_id=current_user.id, opportunity_id=id)
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return bookmark
