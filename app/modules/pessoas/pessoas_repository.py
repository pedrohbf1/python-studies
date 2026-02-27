from sqlalchemy.orm import Session, joinedload
from app.database.models.pessoas import Pessoa
from app.database.models.enderecos import Endereco
from .pessoas_types import getPessoa, PessoaCreate
from typing import Literal
from sqlalchemy.sql.elements import ColumnElement
from typing import Any
from sqlalchemy import update, delete
from typing import Dict

class PessoasRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        return self.db.query(Pessoa).options(joinedload(Pessoa.enderecos)).all()
    
    def listarId(self, id: int):
        return self.db.query(Pessoa).options(joinedload(Pessoa.enderecos)).filter(Pessoa.id == id).first()
        
    
    def getByFilter(self, value: str | int, filter: Literal['email', 'telefone']):
        if filter not in ("email", "telefone"):
            raise ValueError("O filtro deve ser 'email' ou 'telefone'")
        
        field_map: dict[str, ColumnElement[Any]] = {
            "email": Pessoa.email,       # Column[str]
            "telefone": Pessoa.telefone  # Column[int] (ou str se você armazenar como string)
        }

        filterValue = field_map[filter]
        
        return self.db.query(Pessoa).options(joinedload(Pessoa.enderecos)).filter(filterValue == value).first()
    
    def criar(self, pessoa_data: PessoaCreate):
        # Cria uma instância do model Pessoa a partir dos dados recebidos
        nova_pessoa = Pessoa(
            nome=pessoa_data.nome,
            email=pessoa_data.email,
            telefone=pessoa_data.telefone
        )
        self.db.add(nova_pessoa)       # adiciona no DB
        self.db.commit()               # salva
        self.db.refresh(nova_pessoa)   # atualiza a instância com dados do DB (como id)
        if pessoa_data.enderecos:
            for endereco_data in pessoa_data.enderecos:
                novo_endereco = Endereco(
                    rua=endereco_data.rua,
                    bairro=endereco_data.bairro,
                    numero=endereco_data.numero,
                    pessoa_id=nova_pessoa.id
                )
                self.db.add(novo_endereco)
            self.db.commit()            # salva todos os endereços
            self.db.refresh(nova_pessoa, attribute_names=["enderecos"])  # atualiza lista de endereços

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
        return self.db.query(Pessoa).options(joinedload(Pessoa.enderecos)).filter(Pessoa.id == id).first()

    def apagar_pessoa(self, id:int) -> Dict[str, str]:
        self.db.execute(delete(Pessoa).where(Pessoa.id == id))

        self.db.commit()

        return {"message": 'conclued'}