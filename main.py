from fastapi import FastAPI, HTTPException, status
from typing import List
from models import (
    CourseCreate,
    CourseResponse,
    StudentCreate,
    StudentResponse,
    EnrollmentCreate,
    EnrollmentResponse,
    StudentCourseDetail,
)
from database import db

app = FastAPI(
    title="Course Enrollment API",
    description="A FastAPI service for managing courses, student enrollments, and course registrations.",
    version="1.0.0",
)


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Welcome to Course Enrollment API",
        "docs": "/docs",
        "endpoints": [
            "POST /courses",
            "GET /courses",
            "POST /enroll",
            "GET /students/{student_id}/courses",
            "DELETE /enroll/{enrollment_id}",
        ],
    }


# Course endpoints
@app.post("/courses", response_model=CourseResponse, status_code=status.HTTP_201_CREATED, tags=["Courses"])
def create_course(course: CourseCreate):
    """
    Create a new course.
    """
    return db.create_course(course)


@app.get("/courses", response_model=List[CourseResponse], tags=["Courses"])
def list_courses():
    """
    Retrieve all courses.
    """
    return db.list_courses()


# Student endpoints (utility to support student management)
@app.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED, tags=["Students"])
def create_student(student: StudentCreate):
    """
    Create a new student.
    """
    return db.create_student(student)


@app.get("/students", response_model=List[StudentResponse], tags=["Students"])
def list_students():
    """
    List all students.
    """
    return db.list_students()


# Enrollment endpoints
@app.post("/enroll", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED, tags=["Enrollments"])
def enroll_student(enrollment_in: EnrollmentCreate):
    """
    Enroll a student into a course.
    - Validates student existence (404 if not found).
    - Validates course existence (404 if not found).
    - Prevents duplicate enrollments (400 Bad Request).
    """
    student = db.get_student(enrollment_in.student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {enrollment_in.student_id} not found",
        )

    course = db.get_course(enrollment_in.course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {enrollment_in.course_id} not found",
        )

    if db.is_enrolled(enrollment_in.student_id, enrollment_in.course_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student {enrollment_in.student_id} is already enrolled in course {enrollment_in.course_id}",
        )

    return db.enroll_student(enrollment_in.student_id, enrollment_in.course_id)


@app.get(
    "/students/{student_id}/courses",
    response_model=List[StudentCourseDetail],
    tags=["Enrollments"],
)
def get_student_courses(student_id: int):
    """
    Get all courses a specific student is enrolled in.
    - Validates student existence (404 if not found).
    """
    student = db.get_student(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found",
        )

    return db.get_student_courses(student_id)


@app.delete("/enroll/{enrollment_id}", status_code=status.HTTP_200_OK, tags=["Enrollments"])
def delete_enrollment(enrollment_id: int):
    """
    Cancel an enrollment by ID.
    - Returns 404 if enrollment ID does not exist.
    """
    enrollment = db.get_enrollment(enrollment_id)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment with id {enrollment_id} not found",
        )

    db.delete_enrollment(enrollment_id)
    return {"message": f"Enrollment {enrollment_id} has been successfully deleted"}
