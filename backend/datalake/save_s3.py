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
import mimetypes


class SaveS3:
    def __init__(self):
        self.endpoint_url = settings.MINIO_ENDPOINT
        self.fs = s3fs.S3FileSystem(
            client_kwargs={"endpoint_url": self.endpoint_url},
            key=settings.MINIO_ACCESS_KEY,
            secret=settings.MINIO_SECRET_KEY,
            use_ssl=False,
        )

    def upload_file_to_minio(self, bucket_name, object_name, file_data, content_type):
        """
        Uploads file data to MinIO with the correct content type.
        """
        if not file_data:
            raise ValueError("No hay datos para escribir en el archivo.")

        # Asegurarse de incluir el encabezado Content-Disposition como 'inline'
        metadata = {
            "Content-Type": content_type,
            "Content-Disposition": "inline",  # Esto sugiere al navegador mostrar el archivo
        }

        try:
            with self.fs.open(
                f"{bucket_name}/{object_name}",
                "wb",
                metadata=metadata,  # Pasar los metadatos aquí
            ) as f:
                f.write(file_data)
                f.flush()
        except Exception as e:
            raise Exception(f"Error al escribir el archivo en MinIO: {str(e)}")

        return f"{bucket_name}/{object_name}"

    def write_image_to_minio(self, bucket_name, object_name, file_data):
        """
        Handles the full process of writing binary data to MinIO.
        """
        if not file_data:
            raise ValueError("El contenido del archivo está vacío.")

        mime_type, _ = mimetypes.guess_type(object_name)
        if not mime_type:
            mime_type = "application/octet-stream"

        self.fs.makedirs(f"{bucket_name}", exist_ok=True)
        file_path = self.upload_file_to_minio(
            bucket_name, object_name, file_data, mime_type
        )

        return f"http://localhost:9095/{file_path}"

        # http://minio:9000/project-ppe-detection-datalake/images/descarga.jpg
