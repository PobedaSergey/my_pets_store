from pydantic import BaseModel


class User(BaseModel):
    firstname: str = None
    phone: int = None
