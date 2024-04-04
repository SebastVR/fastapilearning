# from typing import Union

# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


from fastapi import FastAPI

# from router import item_router
# from router.router_items import item_router
from router import item_router, file_read_router

app = FastAPI()

app.include_router(
    item_router,
    prefix="/items",  # Define el prefijo para todas las rutas definidas en el router.
    tags=["items"],  # Agrega etiquetas para organizar tus rutas.
)


app.include_router(
    file_read_router,
    prefix="/files",  # Define el prefijo para todas las rutas definidas en el router.
    tags=["files"],  # Agrega etiquetas para organizar tus rutas.
)
