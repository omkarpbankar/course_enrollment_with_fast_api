import pytest
from fastapi.testclient import TestClient
from main import app
from database import db


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    # Setup: clean db state and seed fresh students
    db.clear()
    db._seed_data()
    yield
    # Teardown
    db.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "endpoints" in response.json()


def test_create_course(client):
    payload = {
        "title": "FastAPI Masterclass",
        "description": "Learn to build modern Python APIs",
        "instructor": "John Doe",
    }
    response = client.post("/courses", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["instructor"] == payload["instructor"]


def test_get_courses(client):
    client.post("/courses", json={"title": "Course 1", "instructor": "Inst 1"})
    client.post("/courses", json={"title": "Course 2", "instructor": "Inst 2"})

    response = client.get("/courses")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Course 1"
    assert data[1]["title"] == "Course 2"


def test_enroll_student_success(client):
    course_resp = client.post("/courses", json={"title": "Data Science 101"})
    course_id = course_resp.json()["id"]

    enroll_payload = {"student_id": 1, "course_id": course_id}
    response = client.post("/enroll", json=enroll_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["student_id"] == 1
    assert data["course_id"] == course_id
    assert "enrolled_at" in data


def test_enroll_student_duplicate_prevention(client):
    course_resp = client.post("/courses", json={"title": "Web Dev"})
    course_id = course_resp.json()["id"]

    # First enrollment
    resp1 = client.post("/enroll", json={"student_id": 1, "course_id": course_id})
    assert resp1.status_code == 201

    # Second enrollment (should fail with 400)
    resp2 = client.post("/enroll", json={"student_id": 1, "course_id": course_id})
    assert resp2.status_code == 400
    assert "already enrolled" in resp2.json()["detail"]


def test_enroll_nonexistent_student(client):
    course_resp = client.post("/courses", json={"title": "DevOps"})
    course_id = course_resp.json()["id"]

    response = client.post("/enroll", json={"student_id": 9999, "course_id": course_id})
    assert response.status_code == 404
    assert "Student with id 9999 not found" in response.json()["detail"]


def test_enroll_nonexistent_course(client):
    response = client.post("/enroll", json={"student_id": 1, "course_id": 9999})
    assert response.status_code == 404
    assert "Course with id 9999 not found" in response.json()["detail"]


def test_get_student_courses(client):
    c1 = client.post("/courses", json={"title": "Python Basics", "instructor": "Prof A"}).json()
    c2 = client.post("/courses", json={"title": "Advanced Python", "instructor": "Prof B"}).json()

    client.post("/enroll", json={"student_id": 1, "course_id": c1["id"]})
    client.post("/enroll", json={"student_id": 1, "course_id": c2["id"]})

    # Get student 1 courses
    response = client.get("/students/1/courses")
    assert response.status_code == 200
    courses = response.json()
    assert len(courses) == 2
    titles = [c["title"] for c in courses]
    assert "Python Basics" in titles
    assert "Advanced Python" in titles


def test_get_student_courses_nonexistent_student(client):
    response = client.get("/students/888/courses")
    assert response.status_code == 404
    assert "Student with id 888 not found" in response.json()["detail"]


def test_delete_enrollment_success(client):
    c = client.post("/courses", json={"title": "Machine Learning"}).json()
    enroll = client.post("/enroll", json={"student_id": 1, "course_id": c["id"]}).json()
    enrollment_id = enroll["id"]

    del_resp = client.delete(f"/enroll/{enrollment_id}")
    assert del_resp.status_code == 200
    assert "successfully deleted" in del_resp.json()["message"]

    # Verify courses list for student is now empty
    courses_resp = client.get("/students/1/courses")
    assert courses_resp.status_code == 200
    assert len(courses_resp.json()) == 0

    # Can now re-enroll
    re_enroll = client.post("/enroll", json={"student_id": 1, "course_id": c["id"]})
    assert re_enroll.status_code == 201


def test_delete_nonexistent_enrollment(client):
    response = client.delete("/enroll/9999")
    assert response.status_code == 404
    assert "Enrollment with id 9999 not found" in response.json()["detail"]
