#!/usr/bin/env python3
"""
Script para testar conexão com o banco de dados
"""
import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from config.database import test_connection_personal
    
    print("="*60)
    print("TESTANDO CONEXAO COM O BANCO")
    print("="*60)
    print()
    
    if test_connection_personal():
        print()
        print("="*60)
        print("SUCESSO! Conexao estabelecida.")
        print("="*60)
        sys.exit(0)
    else:
        print()
        print("="*60)
        print("ERRO! Falha na conexao.")
        print("="*60)
        sys.exit(1)
        
except Exception as e:
    print(f"ERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
