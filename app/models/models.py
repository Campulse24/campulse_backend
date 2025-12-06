from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum

# Enums
class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class TaskType(str, Enum):
    CLASS = "Class"
    ASSIGNMENT = "Assignment"
    TEST = "Test"
    EXAM = "Exam"

class OpportunityCategory(str, Enum):
    GIG = "Gig"
    SCHOLARSHIP = "Scholarship"
    TUTOR = "Tutor"
    DEAL = "Deal"

# Models

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: Optional[str] = None
    school: Optional[str] = None
    department: Optional[str] = None
    level: Optional[str] = None
    
    tasks: List["Task"] = Relationship(back_populates="user")
    bookmarks: List["Bookmark"] = Relationship(back_populates="user")

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    due_date: datetime
    priority: Priority = Field(default=Priority.MEDIUM)
    is_completed: bool = Field(default=False)
    type: TaskType = Field(default=TaskType.ASSIGNMENT)

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    
    user: Optional[User] = Relationship(back_populates="tasks")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[Priority] = None
    is_completed: Optional[bool] = None
    type: Optional[TaskType] = None


class Opportunity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    summary: str
    category: OpportunityCategory
    link: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    bookmarks: List["Bookmark"] = Relationship(back_populates="opportunity")

class Tutor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    course: str
    price_range: str
    rating: float = Field(default=0.0)
    whatsapp_contact: str

class Bookmark(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    opportunity_id: int = Field(foreign_key="opportunity.id")
    
    user: Optional[User] = Relationship(back_populates="bookmarks")
    opportunity: Optional[Opportunity] = Relationship(back_populates="bookmarks")
