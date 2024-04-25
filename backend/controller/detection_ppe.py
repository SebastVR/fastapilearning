from pathlib import Path
import shutil
import json
from fastapi import UploadFile
from sqlalchemy.orm import Session
from models.detection_ppe import Project, Detection  # Verifica la ruta de importación
from ultralytics import (
    YOLO,
)  # Asegúrate de tener esta biblioteca correctamente instalada y configurada

from datalake.save_s3 import SaveS3
from datetime import datetime, timedelta

# Configuración del directorio de imágenes
IMAGE_DIR = Path("data/media")
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
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
    """
    Procesa una imagen cargada utilizando YOLO para detectar elementos de protección personal,
    carga la imagen a MinIO y registra los detalles de la detección en la base de datos.
    """
    # Instanciar SaveS3 dentro de la función para utilizarlo para subir el archivo
    s3_saver = SaveS3()

    # Asegúrate de que el directorio existe
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    # Guardar la imagen localmente si es necesario (opcional)
    local_image_path = save_image(file)

    # Cargar la imagen a MinIO y obtener la ruta en el datalake
    bucket_name = "project-ppe-detection-datalake"  # Cambiar por el nombre real de tu bucket en MinIO
    object_name = f"images/{file.filename}"
    datalake_image_path = s3_saver.write_image_to_minio(bucket_name, object_name, file)

    # Procesar la imagen con YOLO
    model = YOLO(MODEL_PATH.as_posix())
    results = model.predict([local_image_path.as_posix()])
    json_data = results[0].tojson()
    detections = json.loads(json_data)

    # Contabilizar los elementos detectados
    detection_counts = {item: 0 for item in EPP_ITEMS}
    for detection in detections:
        if detection["name"] in EPP_ITEMS:
            detection_counts[detection["name"]] += 1

    # Crear un nuevo registro de detección en la base de datos
    new_detection = Detection(
        datalake_image_path=datalake_image_path,
        project_id=project_id,
        **detection_counts,
        created_at=datetime.utcnow(),
    )
    db.add(new_detection)
    db.commit()
    db.refresh(new_detection)

    return new_detection


def save_image(file: UploadFile) -> Path:
    """
    Guarda un archivo cargado localmente y devuelve la ruta al archivo guardado.
    """
    file_location = IMAGE_DIR / file.filename
    with file_location.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_location


##########################################################
###########################################################
########################################################


# def save_image(file: UploadFile) -> Path:
#     """
#     Guarda un archivo cargado y devuelve la ruta al archivo guardado.
#     """
#     file_name = file.filename
#     file_location = IMAGE_DIR / file_name
#     with open(file_location, "wb") as buffer:
#         buffer.write(
#             file.file.read()
#         )  # Escribir el contenido del archivo subido en el nuevo archivo
#         file.file.close()  # Asegurarse de cerrar el archivo subido después de leerlo
#     return file_location


# def process_image(file: UploadFile, db: Session, project_id: int) -> Detection:
#     """
#     Procesa una imagen cargada utilizando YOLO para detectar elementos de protección personal,
#     guarda la ruta de la imagen y registra los detalles de la detección en la base de datos.
#     """

#     file_path = save_image(file)  # Guardar la imagen

#     # Procesar la imagen con YOLO
#     model = YOLO(MODEL_PATH.as_posix())  # Asegúrate de pasar la ruta como string
#     results = model.predict([str(file_path)])
#     json_data = results[0].tojson()
#     detections = json.loads(json_data)

#     # Contabilizar los elementos detectados
#     detection_counts = {item: 0 for item in EPP_ITEMS}  # Inicializar conteos en 0
#     for detection in detections:
#         if detection["name"] in detection_counts:
#             detection_counts[detection["name"]] += 1

#     # Crear un nuevo registro de detección en la base de datos
#     new_detection = Detection(
#         image_path=str(file_path),
#         project_id=project_id,  # Obtener el project_id desde los argumentos de la función
#         **detection_counts,  # Desempaqueta el diccionario directamente en los argumentos del modelo
#     )
#     db.add(new_detection)
#     db.commit()
#     db.refresh(new_detection)

#     return new_detection


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
