from pydantic import BaseModel

class getPessoa(BaseModel):
    nome: str
    email: str
    telefone: int