from repositories.logs import logger
from db.database import SessionLocal


def get_db():
    db = SessionLocal()
    logger.debug("Соединение с базой данных открыто")
    try:
        yield db
    finally:
        db.close()
        logger.debug("Соединение с базой данных закрыто")

