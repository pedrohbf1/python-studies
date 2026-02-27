from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from .pessoas_types import getPessoa, PessoaCreate
from app.database.db import get_db
from app.modules.pessoas.pessoas_repository import PessoasRepository
from app.modules.pessoas.pessoas_service import PessoasService
from typing import Dict

router = APIRouter(prefix="/pessoas", tags=["Pessoas"])

def get_service(db: Session = Depends(get_db)):
    repo = PessoasRepository(db)
    service = PessoasService(repo)
    return service


@router.get("/", response_model=list[getPessoa], summary="Listar todas pessoas")
async def listar(service: PessoasService = Depends(get_service)):
    return service.listar_pessoas()

@router.get("/{id}", response_model=getPessoa, summary="Listar pessoa por id")
async def listarPorId(id: int, service: PessoasService = Depends(get_service)):
    return service.listar_pessoas_id(id)

@router.post("/", response_model=getPessoa, summary="Criar pessoa")
async def criar(service: PessoasService = Depends(get_service), pessoa: PessoaCreate = Body(PessoaCreate)):
    return service.criar(pessoa)

@router.put("/{id}", response_model=getPessoa, summary="Atualizar pessoa por id")
async def atualizar(id: int, service: PessoasService = Depends(get_service), pessoa: getPessoa = Body(getPessoa)):
    return service.atualizar_pessoa(id, pessoa)

@router.delete("/{id}", response_model=Dict[str, str], summary="Deletar pessoa por id")
async def apagar(id: int, service: PessoasService = Depends(get_service)):
    return service.apagar_pessoa(id)