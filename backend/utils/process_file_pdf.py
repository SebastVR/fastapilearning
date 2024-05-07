import pdfplumber
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import camelot


def extract_text(pdf_bytes):
    """Extrae texto de un PDF."""
    text = ""
    with pdfplumber.open(pdf_bytes) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_tables(pdf_path):
    """Extrae tablas de un PDF utilizando Camelot."""
    # Utiliza 'lattice' para PDFs con líneas claras, 'stream' para PDFs sin líneas claras o escaneados
    tables = camelot.read_pdf(pdf_path, flavor="lattice", pages="all")
    if tables.n == 0:  # Si no se encontraron tablas con lattice, intenta con stream
        tables = camelot.read_pdf(pdf_path, flavor="stream", pages="all")
    extracted_tables = [table.df.to_json(orient="records") for table in tables]
    return extracted_tables


def extract_images(pdf_bytes):
    """Extrae todas las imágenes del PDF y aplica OCR para convertirlas en texto."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text_from_images = ""
    for page in doc:
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            text_from_images += pytesseract.image_to_string(image, lang="eng") + "\n"
    return text_from_images


def extract_headers_footers(pdf):
    """Identifica encabezados y pies de página basándose en la posición y repetición."""
    headers, footers = {}, {}
    for page in pdf.pages:
        top_text = []
        bottom_text = []
        text = page.extract_text()
        if text:
            lines = text.split("\n")
            if lines:
                # Dividir la página en tercios y tomar los textos de los tercios superior e inferior
                third = len(lines) // 3
                top_text = lines[:third]
                bottom_text = lines[-third:]

        # Añadir a diccionarios y contar repeticiones
        for line in top_text:
            if line in headers:
                headers[line] += 1
            else:
                headers[line] = 1
        for line in bottom_text:
            if line in footers:
                footers[line] += 1
            else:
                footers[line] = 1

    # Filtrar elementos que aparecen repetidamente como encabezados o pies de página
    headers = [
        text for text, count in headers.items() if count > 1
    ]  # Aparece en más de una página
    footers = [
        text for text, count in footers.items() if count > 1
    ]  # Aparece en más de una página
    return headers, footers


##########################################
# from PIL import Image
# from pdf2image import convert_from_path
# import surya
# from surya.ocr import run_ocr
# from surya.model.detection import segformer
# from surya.model.recognition.model import load_model
# from surya.model.recognition.processor import load_processor


# from PIL import Image
# import numpy as np


# def extract_text_and_tables_surya(pdf_path):
#     images = convert_from_path(pdf_path, dpi=300, fmt="jpeg")
#     extracted_text = ""
#     all_tables = []

#     det_processor, det_model = segformer.load_processor(), segformer.load_model()
#     rec_model, rec_processor = load_model(), load_processor()

#     for image in images:
#         # Convertir la imagen PIL a un arreglo de numpy que pueda ser procesado
#         pil_image = Image.fromarray(np.array(image))
#         predictions = run_ocr(
#             [pil_image],
#             ["spa", "eng"],
#             det_model,
#             det_processor,
#             rec_model,
#             rec_processor,
#         )
#         extracted_text += " ".join([pred["text"] for pred in predictions])
#         # Agregar lógica para extraer tablas si es necesario

#     return extracted_text, all_tables
