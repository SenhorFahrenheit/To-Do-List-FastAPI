from sqlmodel import create_engine, SQLModel, Session
from .model import User, Task

# Definição do nome do arquivo do banco de dados SQLite
sqlite_file_name = "database.db"
# URL de conexão com o banco de dados SQLite
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Criação da engine do banco de dados, com argumento para permitir múltiplas conexões em threads diferentes
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

# Função para criar o banco de dados e as tabelas a partir dos modelos definidos
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Função geradora para obter uma sessão de banco de dados, garantindo que a sessão será fechada após o uso
def get_session():
    with Session(engine) as session:
        yield session
