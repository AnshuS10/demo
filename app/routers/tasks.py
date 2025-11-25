from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database
from . import auth  # Import auth to protect routes

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# --- CREATE (Post) ---
@router.post("/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Create the task model, attaching it to the current user's ID
    new_task = models.Task(**task.dict(), owner_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# --- READ ALL (Get) ---
@router.get("/", response_model=List[schemas.TaskResponse])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Only return tasks belonging to the current user
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).offset(skip).limit(limit).all()
    return tasks

# --- READ ONE (Get) ---
@router.get("/{task_id}", response_model=schemas.TaskResponse)
def read_task(task_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# --- UPDATE (Put) ---
@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task_update: schemas.TaskCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    task_query = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id)
    task = task_query.first()
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update the fields
    task_query.update(task_update.dict(), synchronize_session=False)
    db.commit()
    
    return task_query.first()

# --- DELETE (Delete) ---
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    task_query = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id)
    task = task_query.first()
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_query.delete(synchronize_session=False)
    db.commit()
    return None