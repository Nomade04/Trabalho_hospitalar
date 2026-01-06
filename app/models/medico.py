from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class Medico(Base):
    __tablename__ = "medico"

    id_medico = Column(Integer, Primary_key = True, index = True)
    nome = Column(String(100), nullable= False)
    cmr = Column(String(8), nullable= False, unique= True, index = True)
    especialidade = Column(String(20),nullable=False)
    telefone = Column(String(11), nullable= False)
    email = Column(String(100), nullable = False)