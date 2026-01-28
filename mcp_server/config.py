"""
Configurações do servidor MCP
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Configurações do servidor
MCP_PORT = int(os.getenv('MCP_PORT', '8001'))
MCP_HOST = os.getenv('MCP_HOST', '0.0.0.0')

# Configurações do banco de dados
DATABASE_URL_PERSONAL = os.getenv(
    'DATABASE_URL_PERSONAL',
    'postgresql://personal_agent_user:SENHA_SEGURA_AQUI@localhost:5432/personal_agent_db'
)
