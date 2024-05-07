from fastapi import APIRouter, File, UploadFile, HTTPException
from controller.process_file_pdf import process_pdf
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

process_extract_pdf = APIRouter()


@process_extract_pdf.post("/extract-pdf/", response_model=dict)
async def extract_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF.")
    try:
        data = await process_pdf(file)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
