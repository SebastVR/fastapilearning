# from pydantic import BaseSettings
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str

    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_ENDPOINT: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
