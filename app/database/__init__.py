# type: ignore
from .db import engine, Base
from .models import *  # importa todos os models que você quer criar

# Cria todas as tabelas definidas nos models
Base.metadata.create_all(bind=engine)