from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Paciente(Base):
    __tablename__ = "paciente"

    id_paciente = Column(Integer, primary_key=True)
    senha = Column(String(150),nullable=False)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    telefone = Column(String(15), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    consulta = relationship("Consulta", back_populates="paciente")
    notificacoes = relationship("Notificacao", back_populates="paciente")
    prontuario = relationship("Prontuario", back_populates="paciente", uselist=False)