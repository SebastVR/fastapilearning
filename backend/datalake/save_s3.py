import json
from dotenv import dotenv_values
import s3fs
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from fastapi import UploadFile
from core.settings import settings


# class SaveS3:
#     def __init__(self):
#         self.fs = s3fs.S3FileSystem(
#             client_kwargs={"endpoint_url": settings.MINIO_ENDPOINT},
#             key=settings.MINIO_ACCESS_KEY,
#             secret=settings.MINIO_SECRET_KEY,
#             use_ssl=False,
#         )

#     def upload_file_to_minio(self, bucket_name, object_name, file_data):
#         with self.fs.open(f"{bucket_name}/{object_name}", "wb") as f:
#             f.write(file_data)
#         return f"{bucket_name}/{object_name}"

#     def write_image_to_minio(self, bucket_name, object_name, file: UploadFile):
#         object_name = f"images/{file.filename}"
#         file_content = file.file.read()  # Leer el contenido del archivo
#         file_path = self.upload_file_to_minio(bucket_name, object_name, file_content)
#         file.file.close()  # Cerrar el archivo después de leerlo
#         return file_path


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
        with self.fs.open(f"{bucket_name}/{object_name}", "wb") as f:
            f.write(file_data)
        return f"{bucket_name}/{object_name}"

    def write_image_to_minio(self, bucket_name, object_name, file: UploadFile):
        object_name = f"images/{file.filename}"
        file_content = file.file.read()  # Leer el contenido del archivo
        file_path = self.upload_file_to_minio(bucket_name, object_name, file_content)
        file.file.close()  # Cerrar el archivo después de leerlo
        return f"{self.endpoint_url}/{file_path}"


# class SaveS3:
#     def __init__(self, json_data):
#         self.json_data = json_data
#         # self.settings = settings

#     def get_s3_filesystem(self):
#         return s3fs.S3FileSystem(
#             client_kwargs={"endpoint_url": settings.MINIO_ENDPOINT},
#             key=settings.MINIO_ACCESS_KEY,
#             secret=settings.MINIO_SECRET_KEY,
#             use_ssl=False,
#         )

#     def write_image_to_minio(self, bucket_name, object_name, file: UploadFile):
#         file_content = file.file.read()
#         file_path = self.write_to_minio(bucket_name, object_name, file_content)
#         file.file.close()  # No olvides cerrar el archivo después de leerlo.
#         return file_path

#     def write_to_minio(self, bucket_name, object_name):
#         fs = self.get_s3_filesystem()

#         with fs.open(f"{bucket_name}/{object_name}.json", "w") as f:
#             json.dump(self.json_data, f)

#         return "Successfully uploaded as object..."

#     def write_to_minio_parquet(self, bucket_name, object_name):
#         fs = self.get_s3_filesystem()

#         # Asegúrate de que el json_data sea un diccionario o una lista de diccionarios antes de convertirlo a DataFrame
#         if isinstance(self.json_data, str):
#             data_dict = json.loads(self.json_data)
#         elif isinstance(self.json_data, (dict, list)):
#             data_dict = self.json_data
#         else:
#             raise TypeError("json_data must be a dict or a list of dicts")

#         df = pd.DataFrame.from_dict(data_dict)

#         table = pa.Table.from_pandas(df)
#         pq.write_to_dataset(
#             table,
#             root_path=f"{bucket_name}/{object_name}.parquet",
#             filesystem=fs,
#             use_dictionary=True,
#             compression="snappy",
#             version="2.4",
#         )

#         return "Successfully uploaded as parquet file"
