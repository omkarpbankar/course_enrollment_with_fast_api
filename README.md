# Course Enrollment API

A lightweight, modern **FastAPI** application designed to manage courses and student enrollments. It includes duplicate enrollment prevention, relational validation, and comprehensive error responses.

---

## Features

- **Course Management**:
  - `POST /courses`: Create a new course.
  - `GET /courses`: List all available courses.
- **Enrollment Management**:
  - `POST /enroll`: Enroll a student into a course.
  - `GET /students/{student_id}/courses`: View all courses a student is enrolled in.
  - `DELETE /enroll/{enrollment_id}`: Cancel/remove an enrollment.
- **Student Management (Bonus/Utility)**:
  - `POST /students`: Register a new student.
  - `GET /students`: List all registered students.
- **Validation & Error Handling**:
  - Duplicate enrollment prevention (HTTP `400 Bad Request`).
  - Missing student or course validation (HTTP `404 Not Found`).
  - Missing enrollment cancellation validation (HTTP `404 Not Found`).
- **Interactive Documentation**: Interactive Swagger UI (`/docs`) & ReDoc (`/redoc`).
- **Automated Tests**: Comprehensive `pytest` test suite with 100% endpoint test coverage.

---

## Project Structure

```text
course_enrollment_api/
├── main.py              # FastAPI application, route definitions, and error handling
├── models.py            # Pydantic schemas for requests and responses
├── database.py          # In-memory database store and operations
├── test_main.py         # Pytest test cases covering success and error flows
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation and usage guide
```

---

## Installation & Setup

### 1. Prerequisites
- Python 3.10+ (tested with Python 3.12)
- Virtual environment tool (`venv`)

### 2. Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the development server with hot reload:

```bash
uvicorn main:app --reload
```

Once running, access:
- **API Base URL**: `http://127.0.0.1:8000`
- **Interactive API Documentation (Swagger)**: `http://127.0.0.1:8000/docs`
- **Alternative Documentation (ReDoc)**: `http://127.0.0.1:8000/redoc`

> **Note on Initial Data:** The app initializes with two sample students for quick testing:
> - Student ID `1`: `Alice Johnson` (`alice@example.com`)
> - Student ID `2`: `Bob Smith` (`bob@example.com`)

---

## API Reference

### 1. Courses

#### `POST /courses`
Create a new course.

**Request Body:**
```json
{
  "title": "Introduction to Python",
  "description": "Learn fundamentals of Python programming",
  "instructor": "Dr. Angela"
}
```

**Response (`201 Created`):**
```json
{
  "id": 1,
  "title": "Introduction to Python",
  "description": "Learn fundamentals of Python programming",
  "instructor": "Dr. Angela"
}
```

---

#### `GET /courses`
Fetch a list of all courses.

**Response (`200 OK`):**
```json
[
  {
    "id": 1,
    "title": "Introduction to Python",
    "description": "Learn fundamentals of Python programming",
    "instructor": "Dr. Angela"
  }
]
```

---

### 2. Enrollments

#### `POST /enroll`
Enroll a student in a course.

**Request Body:**
```json
{
  "student_id": 1,
  "course_id": 1
}
```

**Response (`201 Created`):**
```json
{
  "id": 1,
  "student_id": 1,
  "course_id": 1,
  "enrolled_at": "2026-10-18T10:30:00Z"
}
```

**Error Responses:**
- **404 Not Found**: If either the student or course doesn't exist:
  ```json
  {
    "detail": "Student with id 99 not found"
  }
  ```
  ```json
  {
    "detail": "Course with id 99 not found"
  }
  ```
- **400 Bad Request**: If the student is already enrolled in the specified course:
  ```json
  {
    "detail": "Student 1 is already enrolled in course 1"
  }
  ```

---

#### `GET /students/{student_id}/courses`
Retrieve all courses that a given student is currently enrolled in.

**Response (`200 OK`):**
```json
[
  {
    "enrollment_id": 1,
    "course_id": 1,
    "title": "Introduction to Python",
    "description": "Learn fundamentals of Python programming",
    "instructor": "Dr. Angela",
    "enrolled_at": "2026-10-18T10:30:00Z"
  }
]
```

**Error Responses:**
- **404 Not Found**: If the student ID does not exist:
  ```json
  {
    "detail": "Student with id 99 not found"
  }
  ```

---

#### `DELETE /enroll/{enrollment_id}`
Cancel an enrollment by ID.

**Response (`200 OK`):**
```json
{
  "message": "Enrollment 1 has been successfully deleted"
}
```

**Error Responses:**
- **404 Not Found**: If the enrollment ID does not exist:
  ```json
  {
    "detail": "Enrollment with id 99 not found"
  }
  ```

---

## Running the Tests

Run the test suite using `pytest`:

```bash
pytest -v
```

All 11 tests check for:
- Course creation and retrieval
- Successful enrollment
- Duplicate enrollment prevention (400)
- Enrollment with non-existent student/course (404)
- Student course listing and non-existent student check (404)
- Enrollment deletion and cancellation verification
