# app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from mysql.connector.errors import IntegrityError, Error as MySQLError

from db import (
    init_db,
    fetch_all_employees,
    fetch_employee_by_id,
    insert_employee,
    update_employee_by_id,
    delete_employee_by_id,
)

app = FastAPI(title="Employees API (FastAPI + MySQL)")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend folder
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def home():
    return FileResponse("frontend/index.html")


# Employee model (same fields; id is optional for create/update)
class Employee(BaseModel):
    id: int | None = None
    name: str
    age: int
    position: str
    department: str
    email: str
    salary: float
    experience: int


# Initialize DB on startup
@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/employees")
def get_all():
    try:
        return fetch_all_employees()
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/employees/{emp_id}")
def get_one(emp_id: int):
    try:
        emp = fetch_employee_by_id(emp_id)
        if not emp:
            raise HTTPException(404, "Employee not found")
        return emp
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/employees")
def create(emp: Employee):
    try:
        # Ignore id from the request payload; DB will assign
        data = emp.dict(exclude={"id"})
        created = insert_employee(data)
        return created
    except IntegrityError as e:
        # e.errno == 1062 for duplicate entry (e.g., email unique)
        raise HTTPException(status_code=400, detail="Email already exists")
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/employees/{emp_id}")
def update(emp_id: int, updated: Employee):
    try:
        # Ensure employee exists
        existing = fetch_employee_by_id(emp_id)
        if not existing:
            raise HTTPException(404, "Employee not found")

        data = updated.dict(exclude={"id"})
        result = update_employee_by_id(emp_id, data)
        if result is None:
            raise HTTPException(404, "Employee not found")
        return result
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/employees/{emp_id}")
def delete(emp_id: int):
    try:
        ok = delete_employee_by_id(emp_id)
        if not ok:
            raise HTTPException(404, "Employee not found")
        return {"message": "Employee deleted"}
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=str(e))