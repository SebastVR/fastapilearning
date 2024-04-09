from fastapi import APIRouter, File as FastAPIFile, UploadFile, Depends
from sqlalchemy.orm import Session
from core.dependencies import get_db
from controller.file_read import read_pdf_and_save

file_router = APIRouter()


@file_router.post("/pdf")
async def read_pdf(file: UploadFile = FastAPIFile(...), db: Session = Depends(get_db)):
    file_data = await file.read()
    pdf_contents = read_pdf_and_save(file_data, file.filename, db)
    return {"pdf_contents": pdf_contents}
