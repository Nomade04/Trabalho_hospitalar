from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Administracao(Base):
    __tablename__="administracao"

    id_admin = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    cargo = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    relatorio = relationship("Relatorio", back_populates="administracao")
    leito = relationship("Leito", back_populates="administracao")
    estoque = relationship("Estoque", back_populates="administracao")
