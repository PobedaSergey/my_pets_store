from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

from db.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    pets = relationship("PetModel", back_populates="owner")