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
import cv2
import datetime as dt

# Configuración del directorio de imágenes
# IMAGE_DIR = Path("data/media")
# IMAGE_DIR.mkdir(parents=True, exist_ok=True)
# MODEL_PATH = Path("data/staticfiles/best.pt")

IMAGE_DIR = Path("data/media")
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = Path("data/staticfiles/best_runs_79E_ML_5255IMG_15-05-2024.pt")

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


##############################################################
##############################################################


def save_image_from_frame(frame, cont) -> Path:
    unique_filename = f"{uuid4()}_IMG_{cont:04d}.jpg"
    file_location = IMAGE_DIR / unique_filename
    cv2.imwrite(str(file_location), frame)
    return file_location


def process_images_from_video(db: Session, project_id: int):
    s3_saver = SaveS3()
    capture = cv2.VideoCapture("http://192.168.2.101:4747/video")
    # model = YOLO(Path().as_posix())
    model = YOLO(MODEL_PATH.as_posix())
    cont = 0
    tiempoA = dt.datetime.now()  # Tiempo de inicio del proceso
    max_duration = dt.timedelta(seconds=25)  # Duración máxima del vídeo
    interval_duration = dt.timedelta(seconds=5)  # Intervalo de captura
    tiempo_ultima_captura = dt.datetime.now()  # Tiempo de la última captura

    while capture.isOpened():
        tiempo_actual = dt.datetime.now()
        tiempo_total_transcurrido = tiempo_actual - tiempoA
        tiempo_desde_ultima_captura = tiempo_actual - tiempo_ultima_captura

        if tiempo_total_transcurrido >= max_duration:
            logging.info("Maximum duration reached, stopping video capture.")
            break

        # if tiempo_desde_ultima_captura >= interval_duration:
        ret, frame = capture.read()
        if not ret:
            logging.error("Failed to capture image from video stream.")
            break

        img_file = save_image_from_frame(frame, cont)
        datalake_image_path_procesada = (
            Path("data/processed") / f"procesada_{uuid4()}_{img_file.name}"
        )
        results = model.predict(
            [img_file.as_posix()],
            save=True,
            project=datalake_image_path_procesada.as_posix(),
        )

        processed_files = list(datalake_image_path_procesada.glob("**/*"))
        datalake_image_processed = "No processed image found"
        for processed_file in processed_files:
            if processed_file.is_file():
                with open(processed_file, "rb") as processed_img_file:
                    datalake_image_processed = s3_saver.write_image_to_minio(
                        "project-ppe-detection-datalake",
                        f"procesada/{uuid4()}_{processed_file.name}",
                        processed_img_file.read(),
                    )
                break

        object_name_original = f"original/{img_file.name}"
        with open(img_file, "rb") as img_file_obj:
            datalake_image_path = s3_saver.write_image_to_minio(
                "project-ppe-detection-datalake",
                object_name_original,
                img_file_obj.read(),
            )

        json_data = results[0].tojson()
        detections = json.loads(json_data)
        detection_counts = {item: 0 for item in EPP_ITEMS}
        for detection in detections:
            if detection["name"] in detection_counts:
                detection_counts[detection["name"]] += 1

        new_detection = Detection(
            datalake_image_path=datalake_image_path,
            datalake_image_processed=datalake_image_processed,
            project_id=project_id,
            created_at=dt.datetime.utcnow(),
            **detection_counts,
        )
        db.add(new_detection)
        db.commit()
        db.refresh(new_detection)

        cont += 1
        tiempo_ultima_captura = (
            dt.datetime.now()
        )  # Actualiza el tiempo después de cada captura

        if cv2.waitKey(1) == ord("s"):
            logging.info("Stopping video capture manually.")
            break

    capture.release()
    cv2.destroyAllWindows()
    logging.info(f"Total images captured and processed: {cont}")
