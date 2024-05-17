from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from controller.detection_ppe import process_image, create_project, get_project
from core.dependencies import get_db
from fastapi import APIRouter, HTTPException, Depends, Request
from models.detection_ppe import Detection

detection_router = APIRouter()


# project_router = APIRouter()


@detection_router.post("/api/detections/{project_id}", status_code=201)
async def create_detection(
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        detection = process_image(file, db, project_id)
        return {
            "id": detection.id,
            "datalake_image_path": detection.datalake_image_path,
            "datalake_image_processed": detection.datalake_image_processed,
            "arnes": detection.arnes,
            "barbuquejo": detection.barbuquejo,
            "botas": detection.botas,
            "casco": detection.casco,
            "chaleco": detection.chaleco,
            "eslingas": detection.eslingas,
            "guantes": detection.guantes,
            "personas": detection.personas,
            "proteccion_auditiva": detection.proteccion_auditiva,
            "proteccion_respiratoria": detection.proteccion_respiratoria,
            "proteccion_visual": detection.proteccion_visual,
            "project_id": detection.project_id,
            "created_at": detection.created_at.isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@detection_router.get("/api/detections/{detection_id}")
async def get_detection_details(detection_id: int, db: Session = Depends(get_db)):
    try:
        detection = db.query(Detection).filter(Detection.id == detection_id).first()
        if detection is None:
            raise HTTPException(status_code=404, detail="Detection not found")
        return {
            "id": detection.id,
            "datalake_image_path": detection.datalake_image_path,
            "datalake_image_processed": detection.datalake_image_processed,
            "arnes": detection.arnes,
            "barbuquejo": detection.barbuquejo,
            "botas": detection.botas,
            "casco": detection.casco,
            "chaleco": detection.chaleco,
            "eslingas": detection.eslingas,
            "guantes": detection.guantes,
            "personas": detection.personas,
            "proteccion_auditiva": detection.proteccion_auditiva,
            "proteccion_respiratoria": detection.proteccion_respiratoria,
            "proteccion_visual": detection.proteccion_visual,
            "project_id": detection.project_id,
            "created_at": detection.created_at.isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    code: str
    location: str
    phone: str


@detection_router.post("/api/projects/")
async def create_project_endpoint(
    project_data: ProjectCreate, db: Session = Depends(get_db)
):
    # data = await request.json()
    project = create_project(
        db,
        name=project_data.name,
        code=project_data.code,
        location=project_data.location,
        phone=project_data.phone,
    )
    return {
        "id": project.id,
        "name": project.name,
        "code": project.code,
        "location": project.location,
        "phone": project.phone,
    }


@detection_router.get("/api/projects/{project_id}")
async def get_project_endpoint(project_id: int, db: Session = Depends(get_db)):
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {
        "id": project.id,
        "name": project.name,
        "code": project.code,
        "location": project.location,
        "phone": project.phone,
    }
