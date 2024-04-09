from fastapi import APIRouter, File as FastAPIFile, UploadFile, Depends
from sqlalchemy.orm import Session
from core.dependencies import get_db
from controller.file_read import read_pdf_and_save
from models.file_read import File


file_router = APIRouter()


@file_router.post("/pdf")
async def read_pdf(file: UploadFile = FastAPIFile(...), db: Session = Depends(get_db)):
    file_data = await file.read()
    pdf_contents = read_pdf_and_save(file_data, file.filename, db)
    return {"values": pdf_contents}


@file_router.get("/pdf")
async def read_pdf_get(db: Session = Depends(get_db)):
    files = db.query(File).all()
    return {"values": [file.title for file in files]}
