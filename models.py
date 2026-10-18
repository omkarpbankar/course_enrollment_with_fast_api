from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CourseCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Course title")
    description: Optional[str] = Field(default="", description="Course description")
    instructor: Optional[str] = Field(default="", description="Instructor name")


class CourseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = ""
    instructor: Optional[str] = ""


class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Student name")
    email: Optional[str] = Field(default=None, description="Student email")


class StudentResponse(BaseModel):
    id: int
    name: str
    email: Optional[str] = None


class EnrollmentCreate(BaseModel):
    student_id: int = Field(..., description="ID of student enrolling")
    course_id: int = Field(..., description="ID of course to enroll in")


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime


class StudentCourseDetail(BaseModel):
    enrollment_id: int
    course_id: int
    title: str
    description: Optional[str] = ""
    instructor: Optional[str] = ""
    enrolled_at: datetime
