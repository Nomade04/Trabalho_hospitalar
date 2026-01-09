# seed.py (senhas criptografadas — exige String(128) nos models)
import datetime
from app.database import SessionLocal
from app.models.paciente import Paciente
from app.models.medico import Medico
from app.models.administracao import Administracao
from app.security import hash_senha

def popular_banco():
    db = SessionLocal()

    # Pacientes (3)
    pacientes = [
        Paciente(
            nome="Maria Silva",
            cpf="12345678901",
            data_nascimento=datetime.date(1990, 5, 12),
            telefone="11987654321",
            email="maria@hospital.com",
            senha=hash_senha("senhaMaria")
        ),
        Paciente(
            nome="Carlos Souza",
            cpf="23456789012",
            data_nascimento=datetime.date(1985, 8, 23),
            telefone="11999887766",
            email="carlos@hospital.com",
            senha=hash_senha("senhaCarlos")
        ),
        Paciente(
            nome="Ana Lima",
            cpf="34567890123",
            data_nascimento=datetime.date(1998, 2, 3),
            telefone="11988776655",
            email="ana.lima@hospital.com",
            senha=hash_senha("senhaAna")
        ),
    ]

    # Médicos (3)
    medicos = [
        Medico(
            nome="Dr. João Pereira",
            cmr="12345678",
            especialidade="Cardiologia",
            telefone="11987650000",
            email="joao@hospital.com",
            senha=hash_senha("123456")
        ),
        Medico(
            nome="Dra. Ana Borges",
            cmr="23456789",
            especialidade="Pediatria",
            telefone="11987651111",
            email="ana@hospital.com",
            senha=hash_senha("senhaAna")
        ),
        Medico(
            nome="Dr. Marcos Teixeira",
            cmr="34567890",
            especialidade="Ortopedia",
            telefone="11987652222",
            email="marcos@hospital.com",
            senha=hash_senha("senhaMarcos")
        ),
    ]

    # Administração (3)
    admins = [
        Administracao(
            nome="Administrador 1",
            cargo="Gerente",
            email="admin1@hospital.com",
            senha=hash_senha("admin123")
        ),
        Administracao(
            nome="Administrador 2",
            cargo="Supervisor",
            email="admin2@hospital.com",
            senha=hash_senha("admin456")
        ),
        Administracao(
            nome="Administrador 3",
            cargo="Diretor",
            email="admin3@hospital.com",
            senha=hash_senha("admin789")
        ),
    ]

    db.add_all(pacientes + medicos + admins)
    db.commit()
    db.close()
    print("Seed concluído com senhas criptografadas.")

if __name__ == "__main__":
    popular_banco()