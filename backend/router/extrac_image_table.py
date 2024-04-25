# router_extrar.py
from fastapi import APIRouter, File, UploadFile
from controller.extrac_image_table import process_pdf

extrac_router = APIRouter()


@extrac_router.post(
    "/api/process-pdf/", summary="Process a PDF file to extract tables and images"
)
async def process_pdf_route(file: UploadFile = File(...)):
    return await process_pdf(file)
