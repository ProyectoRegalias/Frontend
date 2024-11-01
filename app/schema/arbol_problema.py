from pydantic import BaseModel


class ArbolProblemaBase(BaseModel):
    id:int
    id_proyecto:int


class ArbolProblemaSchema(ArbolProblemaBase):
    id: int

    class Config:
        orm_mode = True