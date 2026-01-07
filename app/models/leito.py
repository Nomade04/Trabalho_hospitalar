from sqlalchemy import Column, Integer,Boolean, String
from sqlalchemy.orm import relationship
from app.database import Base

class Leito(Base):
    __tablename__ = "leito"

    id = Column(Integer, primary_key=True)
    status_vago = Column(Boolean, nullable=False)
    localizacao = Column(String, nullable=False)

    administracao = relationship("Administracao", back_populates="leito")