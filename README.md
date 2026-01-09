# Trabalho_hospitalar
Criação de sistema back-end com proposito didático

# 🏥 Sistema de Gestão Hospitalar

Este projeto é uma API desenvolvida em **Python** utilizando **FastAPI** para gerenciar informações hospitalares, como pacientes, médicos e consultas.  
O objetivo é fornecer uma base escalável e organizada para aplicações de saúde.

---

## Requerimentos utilizados 
- -[Python 3.13](https://www.python.org/) – versão utilizada no ambiente 
- - [FastAPI 0.115.5](https://fastapi.tiangolo.com/) – framework principal da API 
- - [Uvicorn 0.30.0](https://www.uvicorn.org/) – servidor ASGI para rodar a aplicação 
- - [SQLAlchemy 2.0.32](https://www.sqlalchemy.org/) – ORM para banco de dados 
- - [PyMySQL 1.1.0](https://pymysql.readthedocs.io/) – driver para MySQL 
- - [SQLAlchemy-Utils 0.41.2](https://sqlalchemy-utils.readthedocs.io/) – utilitários extras para SQLAlchemy 
- - [Pydantic 2.6.4](https://docs.pydantic.dev/) – validação de dados (com suporte a `EmailStr`) 
- - [python-jose 3.3.0](https://python-jose.readthedocs.io/) – geração e validação de tokens JWT 
- - [passlib 1.7.4](https://passlib.readthedocs.io/) – hashing seguro de senhas (com bcrypt) 
- - [cryptography 42.0.5](https://cryptography.io/) – suporte criptográfico 
- - [python-dotenv 1.0.1](https://pypi.org/project/python-dotenv/) – gerenciamento de variáveis de ambiente

---

##  Estrutura de pastas

Trabalho_hospitalar/ │ ├── app/ │   ├── models/ # Definições das tabelas (Paciente, Médico, Consulta) │
├── routes/      # Endpoints da API │   ├── services/    # Regras de negócio │
└── schemas/     # Validações com Pydantic │
├── main.py          # Ponto de entrada da aplicação 
├── requirements.txt # Dependências do projeto └── README.md  # Documentação


---

##  Instalação e execução

### 1. Clonar o repositório
```bash
git clone https://github.com/Nomade04/Trabalho_hospitalar.git
cd Trabalho_hospitalar
```

### 2. Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
### 3. Instalar dependências
```bash 
pip install -r requirements.txt
```
### 4. Rodar o servidor
```bash
uvicorn main:app --reload
```
A API estará disponível em:
- http://127.0.0.1:8000

