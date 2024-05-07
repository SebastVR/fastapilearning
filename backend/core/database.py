from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Asegúrate de ajustar la importación según tu estructura de proyecto
from core.settings import settings

# Usa la propiedad DATABASE_URL de la instancia settings para la conexión
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
