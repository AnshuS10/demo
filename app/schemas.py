from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# --- Token Schemas (For Login Response) ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Task Schemas ---

# Base schema with shared fields
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "Normal"  # Default to Normal
    deadline: Optional[datetime] = None
    completed: bool = False

# Schema for creating a task (Input)
class TaskCreate(TaskBase):
    pass

# Schema for reading a task (Output)
class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        # This tells Pydantic to read data even if it's not a dict, but an ORM model
        from_attributes = True

# --- User Schemas ---

class UserBase(BaseModel):
    email: EmailStr  # EmailStr validates that it is a real email format

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    tasks: List[TaskResponse] = [] # Nested list of tasks

    class Config:
        from_attributes = True