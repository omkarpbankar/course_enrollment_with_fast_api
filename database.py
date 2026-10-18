from datetime import datetime, timezone
from typing import Dict, List, Optional
from models import CourseCreate, CourseResponse, StudentCreate, StudentResponse, EnrollmentResponse, StudentCourseDetail


class Database:
    def __init__(self):
        self.courses: Dict[int, dict] = {}
        self.students: Dict[int, dict] = {}
        self.enrollments: Dict[int, dict] = {}
        self._course_id_seq = 1
        self._student_id_seq = 1
        self._enrollment_id_seq = 1

        # Seed with initial sample students if useful
        self._seed_data()

    def _seed_data(self):
        # Seed 2 sample students so testing enrollments without manual student creation is seamless
        self.create_student(StudentCreate(name="Alice Johnson", email="alice@example.com"))
        self.create_student(StudentCreate(name="Bob Smith", email="bob@example.com"))

    # Student operations
    def create_student(self, student_in: StudentCreate) -> StudentResponse:
        student_id = self._student_id_seq
        self._student_id_seq += 1
        record = {
            "id": student_id,
            "name": student_in.name,
            "email": student_in.email,
        }
        self.students[student_id] = record
        return StudentResponse(**record)

    def get_student(self, student_id: int) -> Optional[StudentResponse]:
        record = self.students.get(student_id)
        if record:
            return StudentResponse(**record)
        return None

    def list_students(self) -> List[StudentResponse]:
        return [StudentResponse(**s) for s in self.students.values()]

    # Course operations
    def create_course(self, course_in: CourseCreate) -> CourseResponse:
        course_id = self._course_id_seq
        self._course_id_seq += 1
        record = {
            "id": course_id,
            "title": course_in.title,
            "description": course_in.description or "",
            "instructor": course_in.instructor or "",
        }
        self.courses[course_id] = record
        return CourseResponse(**record)

    def get_course(self, course_id: int) -> Optional[CourseResponse]:
        record = self.courses.get(course_id)
        if record:
            return CourseResponse(**record)
        return None

    def list_courses(self) -> List[CourseResponse]:
        return [CourseResponse(**c) for c in self.courses.values()]

    # Enrollment operations
    def is_enrolled(self, student_id: int, course_id: int) -> bool:
        return any(
            e["student_id"] == student_id and e["course_id"] == course_id
            for e in self.enrollments.values()
        )

    def enroll_student(self, student_id: int, course_id: int) -> EnrollmentResponse:
        enrollment_id = self._enrollment_id_seq
        self._enrollment_id_seq += 1
        record = {
            "id": enrollment_id,
            "student_id": student_id,
            "course_id": course_id,
            "enrolled_at": datetime.now(timezone.utc),
        }
        self.enrollments[enrollment_id] = record
        return EnrollmentResponse(**record)

    def get_student_courses(self, student_id: int) -> List[StudentCourseDetail]:
        details = []
        for e in self.enrollments.values():
            if e["student_id"] == student_id:
                course = self.courses.get(e["course_id"])
                if course:
                    details.append(
                        StudentCourseDetail(
                            enrollment_id=e["id"],
                            course_id=course["id"],
                            title=course["title"],
                            description=course["description"],
                            instructor=course["instructor"],
                            enrolled_at=e["enrolled_at"],
                        )
                    )
        return details

    def delete_enrollment(self, enrollment_id: int) -> bool:
        if enrollment_id in self.enrollments:
            del self.enrollments[enrollment_id]
            return True
        return False

    def get_enrollment(self, enrollment_id: int) -> Optional[EnrollmentResponse]:
        record = self.enrollments.get(enrollment_id)
        if record:
            return EnrollmentResponse(**record)
        return None

    def clear(self):
        self.courses.clear()
        self.students.clear()
        self.enrollments.clear()
        self._course_id_seq = 1
        self._student_id_seq = 1
        self._enrollment_id_seq = 1


db = Database()
