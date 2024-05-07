import tempfile
import shutil
from PIL import Image
import pandas as pd
from io import BytesIO
from unstructured_client import UnstructuredClient
from unstructured.staging.base import dict_to_elements
from unstructured_client.models import shared

# from Utils import Utils

# import utils


class Utils:
    def get_dlai_api_key(self):
        """
        Retorna None porque en el entorno local no se requiere clave API.
        """
        return "eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcHAiLCJzdWIiOiIxOTAzNzAyIiwiYXVkIjoiV0VCIiwiaWF0IjoxNzEzNTMxOTMxLCJleHAiOjE3MTYxMjM5MzF9.6fJtH_96RkiKwU1aCFFHjVuPYsD7Si3gT6BeF-dNfPU"

    def get_dlai_url(self):
        """
        Retorna la URL del servidor local donde está desplegada la API para el procesamiento de documentos.
        Este valor debería ser actualizado si cambias la dirección de la API o si la mueves a producción.
        """
        return "http://jupyter-api-proxy.internal.dlai/rev-proxy/unstructured"


utils = Utils()


def initialize_client():
    # Suponiendo que tienes un método para obtener la API KEY y URL
    DLAI_API_KEY = utils.get_dlai_api_key()
    DLAI_API_URL = utils.get_dlai_url()
    client = UnstructuredClient(api_key_auth=DLAI_API_KEY, server_url=DLAI_API_URL)
    return client


pdf_path = "/app/pdf-ensayo.pdf"


def extract_tables(pdf_path):
    client = initialize_client()
    with open(pdf_path, "rb") as f:
        files = shared.Files(
            content=f.read(),
            file_name=pdf_path,
        )
    req = shared.PartitionParameters(
        files=files,
        strategy="hi_res",
        hi_res_model_name="yolox",
        pdf_infer_table_structure=True,
    )
    try:
        resp = client.general.partition(req)
        if resp.elements:
            elements = dict_to_elements(resp.elements)
            tables = [el for el in elements if el.category == "Table"]
            return tables
        else:
            print("No tables found in the PDF.")
            return []
    except Exception as e:
        print(f"Failed to extract tables: {e}")
        return []


def extract_images(pdf_path):
    client = initialize_client()
    with open(pdf_path, "rb") as f:
        files = shared.Files(
            content=f.read(),
            file_name=pdf_path,
        )

    req = shared.PartitionParameters(
        files=files,
        strategy="hi_res",
        hi_res_model_name="yolox",
    )

    try:
        resp = client.general.partition(req)
        elements = dict_to_elements(resp.elements)
        images = [el for el in elements if el.category == "Image"]
        return images
    except Exception as e:
        print(f"Failed to extract images: {e}")
        return []


def save_tables_as_excel(tables):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")

    for i, table in enumerate(tables):
        try:
            df = pd.read_html(table.metadata.text_as_html)[0]
            df.to_excel(writer, sheet_name=f"Table_{i}", index=False)
        except ValueError as e:
            print(f"Error processing table {i}: {e}")

    writer.save()
    output.seek(0)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    with open(temp_file.name, "wb") as f:
        f.write(output.read())

    return temp_file.name


def save_images(images):
    if not images:
        return None

    image_data = images[0].content  # Asegúrate de que este sea el formato correcto
    img = Image.open(BytesIO(image_data))
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    img.save(temp_file.name)

    return temp_file.name
