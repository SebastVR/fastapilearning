import fitz  # PyMuPDF
import camelot
from PIL import Image
import io


def extract_images_from_pdf(pdf_path):
    """
    Extrae imágenes directamente del archivo PDF utilizando PyMuPDF.
    Guarda cada imagen extraída como PNG y devuelve los nombres de los archivos.
    """
    doc = fitz.open(pdf_path)
    image_files = []
    for i in range(len(doc)):
        for img_index, img in enumerate(doc.get_page_images(i)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            file_name = f"page_{i}_img_{img_index}.png"
            image.save(file_name, "PNG")
            image_files.append(file_name)
    doc.close()
    return image_files


def extract_tables_from_pdf(pdf_path):
    """
    Utiliza Camelot para extraer tablas de un archivo PDF y las devuelve como listas de DataFrames.
    """
    tables = camelot.read_pdf(pdf_path, pages="all", flavor="stream")
    return [table.df for table in tables]
