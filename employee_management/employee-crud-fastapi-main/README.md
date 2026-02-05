Employee Management System (FastAPI + Premium Frontend)

A modern Employee CRUD (Create, Read, Update, Delete) application built using:

FastAPI (Backend)

HTML, CSS, JavaScript (Frontend)

Modern Premium UI with glassmorphism design

This project allows adding, updating, deleting, and listing employees with extra fields like salary and experience.

📸 UI Preview

Premium UI with a clean dashboard layout, modern card design, and responsive form

(Add your screenshots here later)

✨ Features
🔵 Backend (FastAPI)

Add employee

Get all employees

Edit employee

Delete employee

Clean, simple API

In-memory database

CORS enabled

Serves frontend HTML/CSS/JS

🟣 Frontend (Premium UI)

Modern glassmorphism design

Add employee form

Editable employee table

Beautiful animations

Fully responsive

Fast and smooth UX

🛠️ Tech Stack
Frontend

HTML5

CSS3

JavaScript (Vanilla JS)

Backend

Python 3.x

FastAPI

Pydantic

Uvicorn

📁 Project Structure
project/
│── app.py                # FastAPI backend
│── employees.json        # (optional future DB)
│── frontend/
│     ├── index.html      # UI page
│     ├── style.css       # Premium styled UI
│     └── script.js       # API calls + logic
│
└── README.md

🚀 How to Run the Project
1️⃣ Install Dependencies
pip install fastapi uvicorn pydantic

2️⃣ Start FastAPI Server
uvicorn app:app --reload


Server runs at:

http://localhost:8000

3️⃣ Open Frontend

Simply visit:

http://localhost:8000


Frontend loads automatically because FastAPI serves your HTML/CSS/JS files.

🧠 API Endpoints
Method	Endpoint	Description
GET	/employees	Get all employees
GET	/employees/{id}	Get employee by ID
POST	/employees	Create new employee
PUT	/employees/{id}	Update employee
DELETE	/employees/{id}	Delete employee
🧩 Employee Data Model
{
  "id": 1,
  "name": "Vignesh",
  "age": 25,
  "position": "Developer",
  "department": "IT",
  "email": "test@mail.com",
  "salary": 50000,
  "experience": 2
}

