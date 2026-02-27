from app.modules.pessoas.pessoas_repository import PessoasRepository
from .pessoas_types import getPessoa
from fastapi import HTTPException, status
from typing import Literal

class PessoasService:
    def __init__(self, repo: PessoasRepository):
        self.repo = repo

    def listar_pessoas(self):
        return self.repo.listar()

    def listar_pessoas_id(self, id: int):
        return self.repo.listarId(id)
    
    def criar(self, pessoa_data: getPessoa):
        checks: list[tuple[Literal['email','telefone'], str | int]] = [
            ('email', pessoa_data.email),
            ('telefone', pessoa_data.telefone)
        ]

        for field, value in checks:
            existente = self.repo.getByFilter(value, field)
            if existente:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{field.capitalize()} {value} já está cadastrado"
                )

        return self.repo.criar(pessoa_data)

    def atualizar_pessoa(self, id: int, pessoa_data: getPessoa):
        checks: list[tuple[Literal['email','telefone'], str | int]] = [
            ('email', pessoa_data.email),
            ('telefone', pessoa_data.telefone)
        ]

        for field, value in checks:
            existente = self.repo.getByFilter(value, field)
            if existente:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{field.capitalize()} {value} já está cadastrado"
                )
        return self.repo.atualizar_pessoa(id, pessoa_data)
    
    def apagar_pessoa(self, id:int):
        return self.repo.apagar_pessoa(id)