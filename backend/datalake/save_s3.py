import json
from dotenv import dotenv_values
import s3fs
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from fastapi import UploadFile
from core.settings import settings
from botocore.exceptions import ClientError
import boto3


class SaveS3:
    def __init__(self):
        self.endpoint_url = settings.MINIO_ENDPOINT
        self.fs = s3fs.S3FileSystem(
            client_kwargs={"endpoint_url": self.endpoint_url},
            key=settings.MINIO_ACCESS_KEY,
            secret=settings.MINIO_SECRET_KEY,
            use_ssl=False,
        )

    def upload_file_to_minio(self, bucket_name, object_name, file_data):
        """
        Uploads file data to MinIO.
        """
        if not file_data:
            raise ValueError("No hay datos para escribir en el archivo.")

        try:
            with self.fs.open(f"{bucket_name}/{object_name}", "wb") as f:
                f.write(file_data)
                f.flush()  # Asegurarse de que los datos se escriban completamente
        except Exception as e:
            raise Exception(f"Error al escribir el archivo en MinIO: {str(e)}")

        return f"{bucket_name}/{object_name}"

    def write_image_to_minio(self, bucket_name, object_name, file: UploadFile):
        """
        Handles the full process of reading an image file and writing it to MinIO.
        """
        file.file.seek(0)  # Asegúrate de rebobinar el archivo
        file_content = file.file.read()  # Leer el contenido del archivo

        if not file_content:
            raise ValueError("El contenido del archivo está vacío.")

        # Construir el nombre del objeto con la carpeta 'images/'
        object_name = f"images/{object_name}"

        # Asegurarse de que el directorio de imágenes existe
        self.fs.makedirs(f"{bucket_name}/images", exist_ok=True)

        # Subir el archivo al bucket de MinIO y obtener la ruta en el datalake
        file_path = self.upload_file_to_minio(bucket_name, object_name, file_content)

        file.file.close()  # Cerrar el archivo después de la operación de subida

        return f"http://localhost:9095/{file_path}"  # Devuelve la URL completa accesible desde el navegador
