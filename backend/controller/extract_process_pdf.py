from utils.extract_process_pdf import extract_images_from_pdf, extract_tables_from_pdf


# def process_pdf(pdf_path):
#     """
#     Procesa el PDF para extraer imágenes y tablas.
#     Devuelve las rutas de las imágenes y los DataFrames de las tablas.
#     """
#     image_files = extract_images_from_pdf(pdf_path)
#     tables = extract_tables_from_pdf(pdf_path)
#     table_data = [table.to_dict(orient="records") for table in tables]
#     return table_data, image_files


# def process_pdf(pdf_path):
#     """
#     Procesa el PDF para extraer tablas.
#     Devuelve DataFrames de las tablas extraídas.
#     """
#     tables = extract_tables_from_pdf(pdf_path)
#     return tables


# def process_pdf(pdf_path):
#     """
#     Procesa el PDF para extraer tablas, sincrónicamente.
#     """
#     tables = extract_tables_from_pdf(pdf_path)
#     return tables


import utils
import pandas as pd
from io import BytesIO


def process_pdf_and_convert(pdf_path, format_type):
    """
    Procesa el PDF para extraer tablas y devuelve el archivo en el formato especificado.
    """
    tables = utils.extract_tables_from_pdf(pdf_path)
    if not tables:
        return None

    if format_type == "csv":
        buffer = BytesIO()
        tables[0].to_csv(buffer, index=False, encoding="utf-8")
        buffer.seek(0)
        return buffer

    elif format_type == "xlsx":
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            tables[0].to_excel(writer, index=False)
        buffer.seek(0)
        return buffer

    return None
