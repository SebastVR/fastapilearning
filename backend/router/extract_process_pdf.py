from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from controller.extract_process_pdf import process_pdf_file
from fastapi.responses import JSONResponse

extract_elements = APIRouter()


@extract_elements.post(
    "/process-pdf/",
    response_model=dict,
    responses={200: {"description": "PDF processed successfully"}},
)
async def process_pdf_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="File format not supported. Please upload a PDF file.",
        )

    result = await process_pdf_file(file)
    return JSONResponse(content=result, status_code=200)
