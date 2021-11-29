from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создание URL-адресса базы данных для SQLAlchemy
SQLALCHEMY_DATABASE_URL = "sqlite:///./SQLite_db.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# Создание движка (engine) SQLAlchemy connect_args={"check_same_thread": False} необходим только для SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# Создание локальной сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Создание базового класса
Base = declarative_base()
