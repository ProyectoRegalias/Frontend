from pydantic import BaseModel


class EfectoBase(BaseModel):
    id: int
    id_arbol_problema: int
    tipo: str
    descripcion: str


class EfectoSchema(EfectoBase):
    id: int

    class Config:
        orm_mode = True
