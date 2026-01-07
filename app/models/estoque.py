from sqlalchemy import Column, Integer,String
from sqlalchemy.orm import relationship
from app.database import Base

class Estoque(Base):
    __tablename__ = "estoque"

    id = Column(Integer, primary_key=True)
    nome_item = Column(String(20), nullable=False)
    quantidade = Column(Integer, nullable=False)
    categoria = Column(String(20), nullable=False)

    administracao = relationship("Administracao", back_populates="estoque")

