from sqlalchemy import Column, Integer,ForeignKey,Date,String
from sqlalchemy.orm import relationship
from app.database import Base

class Relatorio(Base):
    __tablename__ = "relatorio"

    id = Column(Integer, primary_key=True)
    tipo = Column(String(500), nullable=False)
    data_geracao = Column(Date, nullable=False)

    id_medico = Column(Integer, ForeignKey("medico.id_medico"), nullable=True)
    id_admin = Column(Integer, ForeignKey("administracao.id_admin"), nullable=True)

    medico = relationship("Medico", back_populates="relatorio")
    administracao = relationship("Administracao", back_populates="relatorio")
