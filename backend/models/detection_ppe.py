from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=True)
    code = Column(String, index=True, nullable=True)
    location = Column(String, index=True, nullable=True)
    phone = Column(String, index=True, nullable=True)

    # Relación con Detection
    detections = relationship("Detection", back_populates="project")

    def save_to_db(self, db: Session):
        """
        Guarda el objeto File en la base de datos.

        :param db: Sesión de la base de datos (dependencia inyectada).
        """
        db.add(self)
        db.commit()
        db.refresh(self)


class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    datalake_image_path = Column(String, index=True)
    arnes = Column(Integer, default=0, nullable=False)
    barbuquejo = Column(Integer, default=0, nullable=False)
    botas = Column(Integer, default=0, nullable=False)
    casco = Column(Integer, default=0, nullable=False)
    chaleco = Column(Integer, default=0, nullable=False)
    eslingas = Column(Integer, default=0, nullable=False)
    guantes = Column(Integer, default=0, nullable=False)
    personas = Column(Integer, default=0, nullable=False)
    proteccion_auditiva = Column(Integer, default=0, nullable=False)
    proteccion_respiratoria = Column(Integer, default=0, nullable=False)
    proteccion_visual = Column(Integer, default=0, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="detections")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Detection(id='{self.id}', datalake_image_path='{self.datalake_image_path}')>"

    def save_to_db(self, db: Session):
        """
        Guarda el objeto File en la base de datos.

        :param db: Sesión de la base de datos (dependencia inyectada).
        """
        db.add(self)
        db.commit()
        db.refresh(self)
