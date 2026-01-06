# Trabalho_hospitalar
Criação de sistema back-end com proposito didático

# 🏥 Sistema de Gestão Hospitalar

Este projeto é uma API desenvolvida em **Python** utilizando **FastAPI** para gerenciar informações hospitalares, como pacientes, médicos e consultas.  
O objetivo é fornecer uma base escalável e organizada para aplicações de saúde.

---

##  Requerimentos utilizados
- [Python 3.13](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/) – servidor ASGI
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM para banco de dados
- [Pydantic](https://docs.pydantic.dev/) – validação de dados
- [sqlalchemy-utils]()
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

