from fastapi import UploadFile
import pdfplumber
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os
from utils.process_file_pdf import (
    extract_text,
    extract_tables,
    extract_images,
    extract_headers_footers,
    # extract_text_and_tables_surya,
)


async def process_pdf(file: UploadFile):
    contents = {"headers": [], "footers": [], "text": "", "tables": [], "images": []}

    # Leer el contenido del archivo PDF desde UploadFile en memoria
    pdf_bytes = await file.read()

    # Trabajar con el PDF directamente desde los bytes para extracción de texto y tablas
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        contents["text"] = extract_text(pdf)
        contents["tables"] = extract_tables(pdf)
        headers_footers = extract_headers_footers(pdf)
        contents["headers"] = headers_footers[0]
        contents["footers"] = headers_footers[1]

    # Para la extracción de imágenes, debido a PyMuPDF, se requiere una ruta de archivo
    # Guarda temporalmente el PDF para esta operación
    temp_path = "temp.pdf"
    with open(temp_path, "wb") as temp_file:
        temp_file.write(pdf_bytes)

    try:
        contents["images"] = extract_images(temp_path)
    finally:
        # Asegurarse de eliminar el archivo temporal después de su uso
        os.remove(temp_path)

    return contents


async def process_pdf(file: UploadFile):
    contents = {"text": "", "tables": []}

    # Guarda el PDF temporalmente
    temp_pdf_path = f"temp_{file.filename}"
    with open(temp_pdf_path, "wb") as f:
        f.write(await file.read())

    # Extraer texto y tablas
    contents["text"] = extract_text(temp_pdf_path)
    contents["tables"] = extract_tables(temp_pdf_path)

    # Eliminar el archivo temporal
    os.remove(temp_pdf_path)

    return contents


#######################################
# from fastapi import UploadFile, HTTPException
# import os
# from utils import extract_text_and_tables_surya


# async def process_pdf(file: UploadFile):
#     temp_pdf_path = f"temp_{file.filename}"
#     try:
#         with open(temp_pdf_path, "wb") as out_file:
#             content = await file.read()
#             out_file.write(content)

#         result = extract_text_and_tables_surya(temp_pdf_path)
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         if os.path.exists(temp_pdf_path):
#             os.remove(temp_pdf_path)
