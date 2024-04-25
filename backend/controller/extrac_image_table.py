import os
import tempfile
import shutil
from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse
from utils.extrac_image_table import (
    extract_tables,
    extract_images,
    save_tables_as_excel,
    save_images,
)


async def process_pdf(file: UploadFile):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(file.file, tmp)
            file_path = tmp.name

        tables = extract_tables(file_path)
        images = extract_images(file_path)

        if tables and images:
            excel_path = save_tables_as_excel(tables)
            image_path = save_images(images)
            return (
                FileResponse(path=excel_path, filename="tables.xlsx"),
                FileResponse(path=image_path, filename="image.png"),
            )
        elif tables:
            excel_path = save_tables_as_excel(tables)
            return FileResponse(path=excel_path, filename="tables.xlsx")
        elif images:
            image_path = save_images(images)
            return FileResponse(path=image_path, filename="image.png")
        else:
            raise HTTPException(
                status_code=404, detail="No tables or images found in the PDF."
            )
    finally:
        file.file.close()
        if os.path.exists(file_path):
            os.remove(file_path)
