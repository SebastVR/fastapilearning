import fitz  # PyMuPDF
import camelot
from PIL import Image
import io
import pdfplumber


def extract_text(pdf_bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


# def extract_tables(pdf_path, method="stream"):
#     tables = camelot.read_pdf(
#         pdf_path, flavor=method, pages="all"
#     )  # Puedes especificar 'stream' o 'lattice'
#     return [table.df for table in tables]
def extract_tables(pdf_path, method="stream"):
    tables = camelot.read_pdf(pdf_path, flavor=method, pages="all")
    return tables


def extract_images(file_path):
    doc = fitz.open(file_path)
    images = []
    for page in doc:
        image_list = page.get_images(full=True)
        for image_index, img in enumerate(image_list, start=1):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            images.append(
                image_bytes
            )  # Podrías guardar las imágenes o devolver como bytes
    doc.close()
    return images


# def extract_tables(pdf_path):
#     """
#     Utiliza Camelot para extraer tablas de un archivo PDF y las devuelve como listas de DataFrames.
#     """
#     tables = camelot.read_pdf(pdf_path, pages="all", flavor="stream")
#     return [table.df for table in tables]


def extract_layout(pdf_path):
    headers, footers, text_blocks = [], [], []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_height = page.height
            header_threshold = (
                page_height * 0.1
            )  # Ajusta estos valores según sea necesario
            footer_threshold = page_height * 0.9

            for block in page.extract_words():  # o 'page.extract_text()'
                block_bottom = block["bottom"]
                block_top = block["top"]
                if block_top < header_threshold:
                    headers.append(block["text"])
                elif block_bottom > footer_threshold:
                    footers.append(block["text"])
                else:
                    text_blocks.append(block["text"])
    return headers, footers, text_blocks
