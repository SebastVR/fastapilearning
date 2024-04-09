from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    file = Column(LargeBinary)

    def save_to_db(self, db: Session):
        """
        Guarda el objeto File en la base de datos.

        :param db: Sesión de la base de datos (dependencia inyectada).
        """
        db.add(self)
        db.commit()
        db.refresh(self)
