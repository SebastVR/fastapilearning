from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    # Configuración de la base de datos
    database_url: PostgresDsn  # Validación automática de DSN PostgreSQL

    # Ejemplo de configuración adicional
    secret_key: str
    debug_mode: bool = False  # Valor predeterminado si DEBUG_MODE no está definido

    class Config:
        # Especifica que Pydantic debería leer las variables de entorno
        # para las configuraciones. Esto es útil si tus configuraciones
        # provienen principalmente de variables de entorno.
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
