import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.detection_ppe import Base, Project, Detection
from router import detection_router
from fastapi import FastAPI
from core.dependencies import get_db, get_test_db

app = FastAPI()
app.include_router(detection_router)


# Dependency override
app.dependency_overrides[get_db] = get_test_db


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


def test_create_project(test_client):
    print("Running test_create_project")
    response = test_client.post(
        "/api/projects/",
        json={
            "name": "Project A",
            "code": "A001",
            "location": "Location A",
            "phone": "1234567890",
        },
    )
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")
    assert response.status_code == 200
    assert response.json()["name"] == "Project A"


def test_get_project(test_client):
    print("Running test_get_project")
    # Create a project first
    response = test_client.post(
        "/api/projects/",
        json={
            "name": "Project B",
            "code": "B001",
            "location": "Location B",
            "phone": "0987654321",
        },
    )
    print(f"Create project response status code: {response.status_code}")
    print(f"Create project response JSON: {response.json()}")

    project_id = response.json()["id"]

    # Fetch the project
    response = test_client.get(f"/api/projects/{project_id}")
    print(f"Fetch project response status code: {response.status_code}")
    print(f"Fetch project response JSON: {response.json()}")
    assert response.status_code == 200
    assert response.json()["name"] == "Project B"


# def test_create_detection(test_client):
#     print("Running test_create_detection")
#     # Create a project first to use in detection
#     response = test_client.post(
#         "/api/projects/",
#         json={
#             "name": "Project C",
#             "code": "C001",
#             "location": "Location C",
#             "phone": "1231231234",
#         },
#     )
#     print(f"Create project response status code: {response.status_code}")
#     print(f"Create project response JSON: {response.json()}")

#     project_id = response.json()["id"]

#     # Create a detection for the project
#     with open("test_image.jpg", "rb") as f:
#         response = test_client.post(
#             f"/api/detections/{project_id}",
#             files={"file": ("test_image.jpg", f, "image/jpeg")},
#         )
#     print(f"Create detection response status code: {response.status_code}")
#     print(f"Create detection response JSON: {response.json()}")

#     assert response.status_code == 201
#     assert response.json()["project_id"] == project_id


# def test_get_detection(test_client):
#     print("Running test_get_detection")
#     # Create a project first to use in detection
#     response = test_client.post(
#         "/api/projects/",
#         json={
#             "name": "Project D",
#             "code": "D001",
#             "location": "Location D",
#             "phone": "3213213214",
#         },
#     )
#     print(f"Create project response status code: {response.status_code}")
#     print(f"Create project response JSON: {response.json()}")

#     project_id = response.json()["id"]

#     # Create a detection for the project
#     with open("test_image.jpg", "rb") as f:
#         response = test_client.post(
#             f"/api/detections/{project_id}",
#             files={"file": ("test_image.jpg", f, "image/jpeg")},
#         )
#     print(f"Create detection response status code: {response.status_code}")
#     print(f"Create detection response JSON: {response.json()}")

#     detection_id = response.json()["id"]

#     # Fetch the detection
#     response = test_client.get(f"/api/detections/{detection_id}")
#     print(f"Fetch detection response status code: {response.status_code}")
#     print(f"Fetch detection response JSON: {response.json()}")
#     assert response.status_code == 200
#     assert response.json()["id"] == detection_id


def test_delete_project(test_client):
    # Primero, creamos un proyecto para luego eliminarlo
    create_response = test_client.post(
        "/api/projects/",
        json={
            "name": "Project C",
            "code": "C001",
            "location": "Location C",
            "phone": "1234567891",
        },
    )
    project_id = create_response.json()["id"]
    print(f"Created project ID: {project_id}")

    # Ahora procedemos a eliminar el proyecto
    delete_response = test_client.delete(f"/api/projects/{project_id}")
    assert delete_response.status_code == 204, "Error deleting the project"

    # Verificar que el proyecto ya no existe
    fetch_response = test_client.get(f"/api/projects/{project_id}")
    assert fetch_response.status_code == 404, "Project still exists after deletion"


# def test_delete_detection(test_client):
#     # Crear un proyecto primero
#     project_response = test_client.post(
#         "/api/projects/",
#         json={
#             "name": "Project for Detection",
#             "code": "D001",
#             "location": "Location D",
#             "phone": "1234567892",
#         },
#     )
#     project_id = project_response.json()["id"]

#     # Crear una detección asociada a ese proyecto
#     detection_response = test_client.post(
#         f"/api/detections/{project_id}",
#         files={"file": ("filename", b"fakeimagecontent", "image/jpeg")},
#     )
#     detection_id = detection_response.json()["id"]
#     print(f"Created detection ID: {detection_id}")

#     # Proceder a eliminar la detección
#     delete_response = test_client.delete(f"/api/detections/{detection_id}")
#     assert delete_response.status_code == 204, "Error deleting the detection"

#     # Verificar que la detección ya no existe
#     fetch_response = test_client.get(f"/api/detections/{detection_id}")
#     assert fetch_response.status_code == 404, "Detection still exists after deletion"
