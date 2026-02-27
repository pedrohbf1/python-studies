from pydantic import BaseModel
from typing import List, Optional

class EnderecoSchema(BaseModel):
    id: int
    rua: str
    bairro: str
    numero: str

    class Config:
        orm_mode = True


class getPessoa(BaseModel):
    nome: str
    email: str
    telefone: int
    enderecos: Optional[List[EnderecoSchema]] = []

    class Config:
        orm_mode = True


class EnderecoCreate(BaseModel):
    rua: str
    bairro: str
    numero: str

class PessoaCreate(BaseModel):
    nome: str
    email: str
    telefone: int
    enderecos: Optional[List[EnderecoCreate]] = []