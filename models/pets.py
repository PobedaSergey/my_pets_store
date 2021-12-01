from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class PetModel(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    animal_name = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("UserModel", back_populates="pets")