from .database import SessionLocal
from .database import TestingSessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency override
def get_test_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
