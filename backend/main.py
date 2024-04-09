from fastapi import FastAPI


from router.file_read import file_router
from router.router_items import item_router

app = FastAPI()

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
