from app.database.db import Base
from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from datetime import datetime
from datetime import datetime, timezone

class Pessoa(Base): 
    __tablename__ = 'pessoas'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True)
    telefone = Column(BigInteger, unique=True, )
    createdAt = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updatedAt = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
