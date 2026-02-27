from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .pessoas_types import getPessoa
from app.database.db import get_db
from app.modules.pessoas.pessoas_repository import PessoasRepository
from app.modules.pessoas.pessoas_service import PessoasService

router = APIRouter(prefix="/pessoas", tags=["Pessoas"])

def get_service(db: Session = Depends(get_db)):
    repo = PessoasRepository(db)
    service = PessoasService(repo)
    return service


@router.get("/", response_model=list[getPessoa])
async def listar(service: PessoasService = Depends(get_service)):
    return service.listar_pessoas()