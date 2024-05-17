from fastapi import FastAPI


from router.file_read import file_router
from router.router_items import item_router
from router.detection_ppe import detection_router
from router.extrac_image_table import extrac_router

# from router.extract_process_pdf import extrac_proccess_pdf
from router.extract_process_pdf import extract_elements
from fastapi.middleware.cors import CORSMiddleware

from router.process_file_pdf import process_extract_pdf

app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:4200",
#     "http://localhost:9001",
#     "http://localhost:80",  # Agrega tu URL local aquí
#     "http://0.0.0.0",
#     "http://0.0.0.0",
#     "http://127.0.0.1",
#     "http://127.0.0.1:9000",
#     "http://127.0.0.1:9001",
# ]

# origins = ["*"]
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    item_router,
    prefix="/items",  # Define el prefijo para todas las rutas definidas en el router.
    tags=["items"],  # Agrega etiquetas para organizar tus rutas.
)


app.include_router(
    file_router,
    prefix="/files",  # Define el prefijo para todas las rutas definidas en el router.
    tags=["files"],  # Agrega etiquetas para organizar tus rutas.
)


app.include_router(
    detection_router,
    prefix="/api",  # Nota: '/api' ya está incluido en las rutas internas del router
    tags=["detections"],
)

# Integración de los routers para projects
# app.include_router(
#     project_router,
#     prefix="/api",  # Nota: si los endpoints ya incluyen '/projects', no repetir aquí
#     tags=["projects"],
# )


app.include_router(
    extrac_router,
    prefix="/api",  # Nota: si los endpoints ya incluyen '/projects', no repetir aquí
    tags=["extrac"],
)

# app.include_router(extrar_router)

# app.include_router(
#     extrac_proccess_pdf,
#     prefix="/api",  # Nota: si los endpoints ya incluyen '/projects', no repetir aquí
#     tags=["extrac"],
# )

# app.include_router(extrar_router)
app.include_router(
    extract_elements,
    prefix="/api",  # Todos los endpoints en este router tendrán este prefijo
    tags=[
        "Extrac PDF Elements"
    ],  # Tag para agruparlos en la documentación automática de FastAPI
)


# app.include_router(extrar_router)
# app.include_router(
#     process_extract_pdf,
#     prefix="/api",  # Todos los endpoints en este router tendrán este prefijo
#     tags=[
#         "Extrac PDF all"
#     ],  # Tag para agruparlos en la documentación automática de FastAPI
# )
