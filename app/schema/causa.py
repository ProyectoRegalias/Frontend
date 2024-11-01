from pydantic import BaseModel


class CausaBase(BaseModel):
    id:int
    id_arbol_problema:int
    tipo:str
    descripcion:str


class ProyectoSchema(CausaBase):
    id: int

    class Config:
        orm_mode = True