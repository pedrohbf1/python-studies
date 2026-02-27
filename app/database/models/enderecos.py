from ..db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

class Endereco(Base):
    __tablename__ = 'enderecos'

    id = Column(Integer, primary_key=True, index=True)
    rua = Column(String)
    bairro = Column(String)
    numero = Column(String)
    pessoa_id = Column(Integer, ForeignKey('pessoas.id'))
    createdAt = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updatedAt = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    pessoa = relationship("Pessoa", back_populates='enderecos')
