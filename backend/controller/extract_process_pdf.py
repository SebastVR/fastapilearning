from fastapi import UploadFile
import io
import fitz  # PyMuPDF
import pdfplumber
from typing import Dict
from utils.extract_process_pdf import (
    extract_text,
    extract_images,
    extract_tables,
    extract_layout,
)
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
import camelot
import base64
import io
import fitz  # PyMuPDF
from typing import Dict

import base64


# async def process_pdf_file(file: UploadFile) -> Dict[str, any]:
async def process_pdf_file(file: UploadFile) -> Dict[str, any]:
    contents = {
        "headers": [],
        "footers": [],
        "text": "",
        "tables": [],
        "images": [],
        "text_blocks": [],
    }

    pdf_bytes = await file.read()

    # Guardar el archivo temporalmente para extracción con Camelot
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    # Extracción de layout
    headers, footers, text_blocks = extract_layout(tmp_path)
    contents["headers"] = headers
    contents["footers"] = footers
    contents["text_blocks"] = text_blocks

    # Extracción de tablas utilizando la función de utilidades
    try:
        camelot_tables = extract_tables(tmp_path, method="stream")
        table_texts = []
        for table in camelot_tables:
            df = table.df
            contents["tables"].append(df.to_dict())
            # Agregar todo el texto de la tabla a una lista para su posterior eliminación del texto principal
            table_texts.extend(df.to_string(index=False, header=False).split("\n"))
    finally:
        os.remove(tmp_path)
    # Extracción de texto usando pdfplumber
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        raw_text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                raw_text += page_text + "\n"

    # Limpiar el texto eliminando las coincidencias con el texto de las tablas
    for table_text in table_texts:
        raw_text = raw_text.replace(table_text, "")

    contents["text"] = raw_text

    # Extracción de imágenes y otros elementos usando PyMuPDF (fitz)
    with fitz.open("pdf", pdf_bytes) as doc:
        for page in doc:
            image_list = page.get_images(full=True)
            for img_ref in image_list:
                xref = img_ref[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                encoded_image = base64.b64encode(image_bytes).decode("utf-8")
                contents["images"].append(encoded_image)

    return {
        "contents": contents,
    }
