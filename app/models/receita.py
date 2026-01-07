from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Receita(Base):
    __tablename__ = "receita"

    id = Column(Integer, primary_key=True)
    medicamentos = Column(String(300), nullable=False)  # ou criar tabela separada
    data_emissao = Column(Date, nullable=False)

    id_consulta = Column(Integer, ForeignKey("consulta.id_consulta"), nullable=False)

    consulta = relationship("Consulta", back_populates="receita")

