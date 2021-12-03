from pydantic import BaseModel as PydanticBaseModel


class ModBaseModel(PydanticBaseModel):
    class Config:
        anystr_strip_whitespace = True
