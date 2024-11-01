from pydantic import BaseModel


class ProyectoBase(BaseModel):
    id:int
    id_usuario:int
    nombre_proyecto:str
    objetico_general:str


class ProyectoSchema(ProyectoBase):
    id: int

    class Config:
        orm_mode = True