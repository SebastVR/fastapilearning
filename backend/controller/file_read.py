import io
from PyPDF2 import PdfFileReader
from sqlalchemy.orm import Session
from models.file_read import File


def read_pdf_and_save(file_data: bytes, filename: str, db: Session):
    pdf_contents = []
    buffer = io.BytesIO(file_data)
    pdf_reader = PdfFileReader(buffer)
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        pdf_contents.append(page.extractText())

    # Crear una instancia del modelo de base de datos y guardarla
    db_file = File(title=filename, file=file_data)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return pdf_contents
