from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Consulta(Base):
    __tablename__ = "consulta"

    id_consulta = Column(Integer, primary_key=True)
    data_hora = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    tipo_presencial = Column(Boolean, nullable=False)

    id_paciente = Column(Integer, ForeignKey("paciente.id_paciente"), nullable=False)
    id_medico = Column(Integer, ForeignKey("medico.id_medico"), nullable=False)

    paciente = relationship("Paciente", back_populates="consulta")
    medico = relationship("Medico", back_populates="consulta")
    receita = relationship("Receita", back_populates="consulta")
