from sqlalchemy.orm import Session
from app.database.models.pessoas import Pessoa
from .pessoas_types import getPessoa
from typing import Literal
from sqlalchemy.sql.elements import ColumnElement
from typing import Any
from sqlalchemy import update, delete
from typing import Dict

class PessoasRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        return self.db.query(Pessoa)
    
    def listarId(self, id: int):
        return self.db.query(Pessoa).filter(Pessoa.id == id).first()
        
    
    def getByFilter(self, value: str | int, filter: Literal['email', 'telefone']):
        if filter not in ("email", "telefone"):
            raise ValueError("O filtro deve ser 'email' ou 'telefone'")
        
        field_map: dict[str, ColumnElement[Any]] = {
            "email": Pessoa.email,       # Column[str]
            "telefone": Pessoa.telefone  # Column[int] (ou str se você armazenar como string)
        }

        filterValue = field_map[filter]
        
        return self.db.query(Pessoa).filter(filterValue == value).first()
    
    def criar(self, pessoa_data: getPessoa):
        # Cria uma instância do model Pessoa a partir dos dados recebidos
        nova_pessoa = Pessoa(
            nome=pessoa_data.nome,
            email=pessoa_data.email,
            telefone=pessoa_data.telefone
        )
        self.db.add(nova_pessoa)       # adiciona no DB
        self.db.commit()               # salva
        self.db.refresh(nova_pessoa)   # atualiza a instância com dados do DB (como id)
        return nova_pessoa

    def atualizar_pessoa(self, id: int, pessoa_data: getPessoa):
        dados = pessoa_data.model_dump(exclude_unset=True)  # Pydantic v2

        self.db.execute(
            update(Pessoa)
            .where(Pessoa.id == id)
            .values(**dados)
        )
        self.db.commit()

        # Retorna a pessoa atualizada
        pessoa_atualizada = self.db.query(Pessoa).filter(Pessoa.id == id).first()
        return pessoa_atualizada

    def apagar_pessoa(self, id:int) -> Dict[str, str]:
        self.db.execute(delete(Pessoa).where(Pessoa.id == id))

        self.db.commit()

        return {"message": 'conclued'}