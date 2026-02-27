import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from typing import Generator
from dotenv import load_dotenv
# Carrega as variáveis do .env
load_dotenv()  
# Pega a URL do banco do .env

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não definida no .env")

# Cria a engine (conexão com o banco)
engine = create_engine(
    url=DATABASE_URL,  # String de conexão com o banco (postgresql+psycopg2://user:pass@host:port/db)

    echo=True,         # Ativa log das queries SQL no terminal
                       # Mostra SELECT, INSERT, UPDATE, parâmetros e transações
                       # Útil para debug em desenvolvimento
                       # Em produção normalmente fica False

    future=True        # Ativa comportamento da API moderna do SQLAlchemy 2.0
                       # Garante uso do novo padrão de execução e sessão
                       # Hoje é opcional no SQLAlchemy 2.x (já é padrão)
)

# Fábrica de sessões
SessionLocal = sessionmaker(
    bind=engine,        # Conecta a sessão à engine (engine = conexão com o banco)

    autoflush=False,    # Impede que alterações sejam enviadas automaticamente
                        # ao banco antes de executar uma query
                        # Dá mais controle manual sobre quando persistir dados

    autocommit=False    # Desativa commit automático após cada operação
                        # Você precisa chamar db.commit() explicitamente
                        # Isso garante controle transacional (boa prática)
)

# Base para todos os models herdarem
class Base(DeclarativeBase):
    pass
    # DeclarativeBase é a classe base do ORM do SQLAlchemy 2.x
    # Todas as entidades (models) devem herdar dela
    # Ela registra automaticamente as tabelas no metadata interno
    # Esse metadata é usado depois para criar as tabelas no banco

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()   # Cria uma nova sessão (transação) com o banco
    try:
        yield db          # Entrega a sessão para a rota que solicitou (Dependency Injection)
    finally:
        db.close()        # Fecha a conexão após a requisição terminar (evita vazamento de conexão)