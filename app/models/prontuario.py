from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Prontuario(Base):
    __tablename__ = "prontuario"

    id = Column(Integer, primary_key=True)
    observacoes = Column(String(500), nullable=False)
    data_atualizacao = Column(Date, nullable=False)

    id_medico = Column(Integer, ForeignKey("medico.id_medico"), nullable=False)
    id_paciente = Column(Integer, ForeignKey("paciente.id_paciente"), nullable=False)

    medico = relationship("Medico", back_populates="prontuario")
    paciente = relationship("Paciente", back_populates="prontuario")
