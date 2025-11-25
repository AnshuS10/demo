# Task & Productivity Planner API

## Overview
A RESTful API built to help users manage tasks and track their productivity. This project demonstrates modular backend architecture using Python.

## Features
* **User Authentication:** Secure signup and login.
* **Task Management:** Add, edit, delete, and view tasks.
* **Productivity Analytics:** View completion statistics.

## Technologies Used
* **Language:** Python
* **Framework:** FastAPI
* **Database:** SQLite (SQLAlchemy)
* **Authentication:** JWT (JSON Web Tokens)

## Steps to Install & Run
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the server: `uvicorn app.main:app --reload`
5. Access API docs at: `http://127.0.0.1:8000/docs`
