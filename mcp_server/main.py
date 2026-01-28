"""
Servidor MCP (Model Context Protocol) para o Agente Pessoal
FastAPI server para detecção, extração, validação e listagem
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os
from pathlib import Path
from dotenv import load_dotenv

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para imports relativos
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.database import SessionLocalPersonal, init_db_personal
from mcp_server.routers import mcp

# Carrega variáveis de ambiente
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Configurações
MCP_PORT = int(os.getenv('MCP_PORT', '8001'))
MCP_HOST = os.getenv('MCP_HOST', '0.0.0.0')


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação
    """
    # Startup: Inicializa banco de dados
    try:
        init_db_personal()
        print("✅ Banco de dados personal_agent_db inicializado")
    except Exception as e:
        print(f"⚠️ Aviso ao inicializar banco: {e}")
    
    yield
    
    # Shutdown: Limpeza se necessário
    pass


# Cria aplicação FastAPI
app = FastAPI(
    title="MCP Server - Agente Pessoal",
    description="Servidor MCP para detecção, extração, validação e listagem de contas a pagar",
    version="1.0.0",
    lifespan=lifespan
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui rotas
app.include_router(mcp.router, prefix="/mcp", tags=["MCP"])


@app.get("/")
async def root():
    """
    Endpoint raiz para verificar se o servidor está rodando
    """
    return {
        "status": "online",
        "service": "MCP Server - Agente Pessoal",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """
    Endpoint de health check
    """
    try:
        # Testa conexão com banco
        from sqlalchemy import text
        db = SessionLocalPersonal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=MCP_HOST,
        port=MCP_PORT,
        reload=True,
        log_level="info"
    )
