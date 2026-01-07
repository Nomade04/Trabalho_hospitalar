from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Notificacao(Base):
    __tablename__ = "notificacao"

    id = Column(Integer, primary_key=True)
    tipo = Column(String(50), nullable=False)
    mensagem = Column(String(300), nullable=False)
    data_envio = Column(DateTime, nullable=False)

    id_paciente = Column(Integer, ForeignKey("paciente.id_paciente"), nullable=False)

    paciente = relationship("Paciente", back_populates="notificacao")

