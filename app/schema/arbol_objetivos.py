from pydantic import BaseModel


class ArbolObjetivoBase(BaseModel):
    id:int
    id_proyecto:int


class ArbolObjetivoSchema(ArbolObjetivoBase):
    id: int

    class Config:
        orm_mode = True