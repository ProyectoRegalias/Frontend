from pydantic import BaseModel


class UsuarioBase(BaseModel):
    username: str
    password: str


class UsuarioSchema(UsuarioBase):
    id: int

    class Config:
        orm_mode = True
