from fastapi import APIRouter, File, UploadFile
from typing import List
import io

# from PyPDF2 import PdfReader
from PyPDF2 import PdfFileReader

file_read_router = APIRouter()


@file_read_router.post("/pdf")
async def read_pdf(file: UploadFile = File(...)):
    """
    Lee un archivo PDF y devuelve el contenido de texto.
    """
    pdf_contents = []
    with io.BytesIO(await file.read()) as buffer:
        buffer.seek(0)
        pdf_reader = PdfFileReader(buffer)
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            pdf_contents.append(page.extractText())
    return {"pdf_contents": pdf_contents}
