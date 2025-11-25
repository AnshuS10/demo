from fastapi import FastAPI
from .database import engine, Base
from .routers import auth, tasks, analytics  


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Productivity Planner API",
    description="A REST API for managing tasks and tracking productivity stats.",
    version="1.0.0"
)


app.include_router(auth.router)       # Module 1: User Management
app.include_router(tasks.router)      # Module 2: Task CRUD
app.include_router(analytics.router)  # Module 3: Analytics


@app.get("/", tags=["General"])
def read_root():
    return {
        "message": "Welcome to the Productivity Planner API!",
        "docs_url": "http://127.0.0.1:8000/docs"
    }