from pathlib import Path
import shutil
import json
from fastapi import UploadFile
from sqlalchemy.orm import Session
from models.detection_ppe import Project, Detection  # Verifica la ruta de importación
from ultralytics import (
    YOLO,
)  # Asegúrate de tener esta biblioteca correctamente instalada y configurada
import logging
from datalake.save_s3 import SaveS3
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
# Configuración del directorio de imágenes
# IMAGE_DIR = Path("data/media")
# IMAGE_DIR.mkdir(parents=True, exist_ok=True)
# MODEL_PATH = Path("data/staticfiles/best.pt")

IMAGE_DIR = Path("data/media")
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = Path("data/staticfiles/best.pt")

# Lista de todos los posibles elementos de EPP
EPP_ITEMS = [
    "arnes",
    "barbuquejo",
    "botas",
    "casco",
    "chaleco",
    "eslingas",
    "guantes",
    "personas",
    "proteccion_auditiva",
    "proteccion_respiratoria",
    "proteccion_visual",
]


def process_image(file: UploadFile, db: Session, project_id: int) -> Detection:
    s3_saver = SaveS3()
    local_image_path = save_image(file)

    # Cargar la imagen original a MinIO
    bucket_name = "project-ppe-detection-datalake"
    object_name_original = f"original/{uuid4()}_{file.filename}"
    with open(local_image_path, "rb") as img_file:
        datalake_image_path = s3_saver.write_image_to_minio(
            bucket_name, object_name_original, img_file.read()
        )

    # Procesar la imagen con YOLO
    datalake_image_path_procesada = (
        PROCESSED_DIR / f"procesada_{uuid4()}_{file.filename}"
    )
    model = YOLO(MODEL_PATH.as_posix())
    results = model.predict(
        [local_image_path.as_posix()],
        save=True,
        project=datalake_image_path_procesada.as_posix(),
    )

    # Revisar qué se ha guardado realmente en el directorio
    processed_files = list(datalake_image_path_procesada.glob("**/*"))
    if processed_files:
        for processed_file in processed_files:
            if (
                processed_file.is_file()
            ):  # Verificar si es un archivo y no un directorio
                with open(processed_file, "rb") as processed_img_file:
                    datalake_image_processed = s3_saver.write_image_to_minio(
                        bucket_name,
                        f"procesada/{uuid4()}_{processed_file.name}",
                        processed_img_file.read(),
                    )
                break
    else:
        datalake_image_processed = "No processed image found"

    # Procesar los resultados
    json_data = results[0].tojson()
    detections = json.loads(json_data)
    detection_counts = {item: 0 for item in EPP_ITEMS}
    for detection in detections:
        if detection["name"] in EPP_ITEMS:
            detection_counts[detection["name"]] += 1

    # Registro en la base de datos
    new_detection = Detection(
        datalake_image_path=datalake_image_path,
        datalake_image_processed=datalake_image_processed,  # Usar la ruta procesada
        project_id=project_id,
        created_at=datetime.utcnow(),
        **detection_counts,
    )
    db.add(new_detection)
    db.commit()
    db.refresh(new_detection)

    return new_detection


from uuid import uuid4


def save_image(file: UploadFile) -> Path:
    unique_filename = f"{uuid4()}_{file.filename}"
    file_location = IMAGE_DIR / unique_filename
    with file_location.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_location


def create_project(
    db: Session, name: str, code: str, location: str, phone: str
) -> Project:
    new_project = Project(name=name, code=code, location=location, phone=phone)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


def get_project(db: Session, project_id: int) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    return project


def delete_project(db: Session, project_id: int) -> None:
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        db.delete(project)
        db.commit()


def delete_detection(db: Session, detection_id: int) -> None:
    detection = db.query(Detection).filter(Detection.id == detection_id).first()
    if detection:
        db.delete(detection)
        db.commit()
