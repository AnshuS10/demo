from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, database
from . import auth

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/productivity")
def get_productivity_stats(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    
    total_tasks = len(tasks)
    if total_tasks == 0:
        return {
            "total_tasks": 0, 
            "completed_tasks": 0, 
            "productivity_score": 0,
            "pending_urgent_tasks": 0
        }

    completed_tasks = sum(1 for t in tasks if t.completed)
    productivity_score = round((completed_tasks / total_tasks) * 100, 2)
    
    pending_urgent = sum(1 for t in tasks if not t.completed and t.priority == "High")

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "productivity_score": f"{productivity_score}%",
        "pending_urgent_tasks": pending_urgent
    }