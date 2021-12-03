from db.database import SessionLocal
from repositories.logs import logger


def get_db():
    db = SessionLocal()
    logger.debug("Соединение с базой данных открыто")
    try:
        yield db
    finally:
        db.close()
        logger.debug("Соединение с базой данных закрыто")

