# from fastapi import APIRouter, File, UploadFile, HTTPException
# from fastapi.responses import JSONResponse, Response
# import os

# from controller.extract_process_pdf import process_pdf
# from controller.extract_process_pdf import process_pdf_and_convert


# extrac_proccess_pdf = APIRouter()


# @extrac_proccess_pdf.post("/api/extact-pdf/", response_model=dict)
# async def process_pdf_route(file: UploadFile = File(...)):
#     temp_file_path = f"temp_{file.filename}"
#     with open(temp_file_path, "wb") as out_file:
#         content = await file.read()
#         out_file.write(content)

#     try:
#         table_data, image_files = process_pdf(temp_file_path)
#         return {"tables": table_data, "image_files": image_files}
#     finally:
#         if os.path.exists(temp_file_path):
#             os.remove(temp_file_path)


# @extrac_proccess_pdf.post("/extract-tables/")
# async def extract_tables_route(file: UploadFile = File(...)):
#     temp_file_path = f"temp_{file.filename}"
#     with open(temp_file_path, "wb") as out_file:
#         content = await file.read()
#         out_file.write(content)

#     try:
#         tables = process_pdf(temp_file_path)
#         # Aseguramos que cada DataFrame se convierte a una lista de diccionarios
#         tables_json = [table.to_dict(orient="records") for table in tables]
#         return {"tables": tables_json}
#     except Exception as e:
#         # Manejo de errores, mostramos el error en la respuesta para facilitar la depuración
#         return JSONResponse(status_code=500, content={"message": str(e)})
#     finally:
#         if os.path.exists(temp_file_path):
#             os.remove(temp_file_path)


# extrac_proccess_pdf = APIRouter()


# @extrac_proccess_pdf.post(
#     "/extract-tables/", responses={200: {"content": {"text/csv": {}}}}
# )
# async def extract_tables_route(file: UploadFile = File(...)):
#     temp_file_path = f"temp_{file.filename}"
#     output_csv_path = f"{temp_file_path}.csv"  # Modificado para claridad

#     with open(temp_file_path, "wb") as out_file:
#         content = await file.read()
#         out_file.write(content)

#     try:
#         tables = process_pdf(
#             temp_file_path
#         )  # Asumiendo que esto sigue siendo sincrónico
#         if tables and not tables[0].empty:
#             tables[0].to_csv(output_csv_path, index=False)
#             if os.path.exists(output_csv_path):  # Verifica que el archivo exista
#                 return FileResponse(
#                     path=output_csv_path,
#                     filename="extracted_table.csv",
#                     media_type="text/csv",
#                 )
#             else:
#                 return Response(content="CSV file was not created.", status_code=500)
#         else:
#             return Response(content="No tables found in the PDF.", status_code=404)
#     finally:
#         # Limpia solo el PDF temporal, no el CSV hasta después del envío
#         if os.path.exists(temp_file_path):
#             os.remove(temp_file_path)


from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import os
from controller.extract_process_pdf import process_pdf_and_convert
from fastapi.responses import JSONResponse, Response


from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import os

extrac_proccess_pdf_router = APIRouter()


@extrac_proccess_pdf_router.post(
    "/extract-tables/", responses={200: {"content": {"application/octet-stream": {}}}}
)
async def extract_tables_route(file: UploadFile = File(...), format: str = None):
    if format not in ["csv", "xlsx"]:
        raise HTTPException(status_code=400, detail="Invalid format specified")

    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as out_file:
        content = await file.read()
        out_file.write(content)

    try:
        file_content = process_pdf_and_convert(temp_file_path, format)
        if file_content is None:
            return StreamingResponse(
                content="No tables found or failed to convert.", status_code=404
            )

        content_type = (
            "text/csv"
            if format == "csv"
            else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response = StreamingResponse(file_content, media_type=content_type)
        response.headers["Content-Disposition"] = (
            f'attachment; filename="extracted_table.{format}"'
        )
        return response

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
