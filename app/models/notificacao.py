from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Notificacao(Base):
    __tablename__ = "notificacao"

    id_notificacao = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("paciente.id_paciente"), nullable=False)
    id_medico = Column(Integer, ForeignKey("medico.id_medico"), nullable=False)
    remetente = Column(String(20), nullable=False)  # "paciente" ou "medico"
    conteudo = Column(String(500), nullable=False)
    data_hora = Column(DateTime, default=datetime.utcnow)

    paciente = relationship("Paciente", back_populates="notificacoes")
    medico = relationship("Medico", back_populates="notificacoes")


