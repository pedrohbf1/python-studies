from sqlalchemy.orm import Session
from app.database.models.pessoas import Pessoa

class PessoasRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        return self.db.query(Pessoa)