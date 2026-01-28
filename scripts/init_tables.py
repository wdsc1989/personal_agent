#!/usr/bin/env python3
"""
Script para inicializar tabelas do banco de dados
Execute no servidor após criar o banco
"""
import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from config.database import test_connection_personal, init_db_personal
    
    print("="*60)
    print("INICIALIZANDO TABELAS DO AGENTE PESSOAL")
    print("="*60)
    print()
    
    print("1. Testando conexão com o banco...")
    if not test_connection_personal():
        print("ERRO: Não foi possível conectar ao banco de dados!")
        print()
        print("Verifique:")
        print("  - PostgreSQL está rodando?")
        print("  - Credenciais no .env estão corretas?")
        print("  - Banco personal_agent_db foi criado?")
        sys.exit(1)
    
    print()
    print("2. Criando tabelas...")
    init_db_personal()
    
    print()
    print("="*60)
    print("SUCESSO! Tabelas criadas.")
    print("="*60)
    print()
    print("Tabelas criadas:")
    print("  - usuarios_telegram")
    print("  - contas_pagar")
    print()
    
except Exception as e:
    print(f"ERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
