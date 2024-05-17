from fastapi import APIRouter, File, UploadFile, HTTPException
from controller.process_file_pdf import process_pdf
from controller.extract_process_pdf import process_pdf_file
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from typing import Dict

from fastapi.responses import JSONResponse

process_extract_pdf = APIRouter()


@process_extract_pdf.post("/extract-pdf/", response_model=dict)
async def extract_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF.")
    try:
        data = await process_pdf_file(file)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @process_extract_pdf.post("/process-pdf/", response_model=Dict[str, any])
# async def process_pdf_endpoint(file: UploadFile = File(...)):
#     if not file.filename.endswith(".pdf"):
#         raise HTTPException(
#             status_code=400,
#             detail="File format not supported. Please upload a PDF file.",
#         )
#     try:
#         result = await process_pdf_file(file)
#         return JSONResponse(content={"contents": result}, status_code=200)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
