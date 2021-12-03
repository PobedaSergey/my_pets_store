from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String

from db.database import Base


class PetModel(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True)
    animal_name = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("UserModel", back_populates="pets")