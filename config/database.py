"""
Configuração do banco de dados personal_agent_db (PostgreSQL)
Banco separado do contabil_db para o agente pessoal
"""
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# URL do banco de dados personal_agent_db
# Formato: postgresql://usuario:senha@host:porta/database
# Exemplo: postgresql://personal_agent_user:senha123@localhost:5432/personal_agent_db
DATABASE_URL_PERSONAL = os.getenv(
    'DATABASE_URL_PERSONAL',
    'postgresql://personal_agent_user:SENHA_SEGURA_AQUI@localhost:5432/personal_agent_db'
)

# Configuração do engine para personal_agent_db
engine_personal = create_engine(
    DATABASE_URL_PERSONAL,
    echo=False,  # Set to True para debug SQL
    pool_pre_ping=True,  # Verifica conexões antes de usar
    pool_size=10,  # Tamanho do pool de conexões
    max_overflow=20,  # Conexões adicionais permitidas
    pool_recycle=3600  # Recicla conexões após 1 hora
)

# Session factory para personal_agent_db
SessionLocalPersonal = sessionmaker(autocommit=False, autoflush=False, bind=engine_personal)

# Base declarativa para modelos do agente pessoal
BasePersonal = declarative_base()


def get_db_personal():
    """
    Dependency para obter uma sessão do banco de dados personal_agent_db
    """
    db = SessionLocalPersonal()
    try:
        yield db
    finally:
        db.close()


def column_exists_personal(table_name: str, column_name: str) -> bool:
    """Verifica se uma coluna existe em uma tabela do banco personal"""
    try:
        inspector = inspect(engine_personal)
        if not inspector.has_table(table_name):
            return False
        columns = [col['name'] for col in inspector.get_columns(table_name)]
        return column_name in columns
    except:
        return False


def init_db_personal():
    """
    Inicializa o banco de dados personal_agent_db criando todas as tabelas
    """
    from models.personal_agent_mvp import UsuarioTelegram, ContaPagar
    BasePersonal.metadata.create_all(bind=engine_personal)
    print("✅ Tabelas do agente pessoal criadas com sucesso!")


def test_connection_personal():
    """
    Testa a conexão com o banco personal_agent_db
    """
    try:
        with engine_personal.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
            print("✅ Conexão com personal_agent_db estabelecida com sucesso!")
            return True
    except Exception as e:
        print(f"❌ Erro ao conectar com personal_agent_db: {e}")
        return False
