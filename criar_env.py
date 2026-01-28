"""
Script para criar arquivo .env rapidamente
"""
import sys
from pathlib import Path

def criar_env_rapido(host="srv1140258.hstgr.cloud", porta="5432", 
                     banco="personal_agent_db", usuario="personal_agent_user", 
                     senha=None, mcp_port="8001", mcp_host="0.0.0.0"):
    """Cria arquivo .env com valores fornecidos"""
    env_path = Path(__file__).parent / '.env'
    
    if not senha:
        print("ATENCAO: Senha nao fornecida. Usando valor padrao.")
        print("IMPORTANTE: Altere a senha no arquivo .env depois!")
        senha = "SENHA_SEGURA_AQUI"
    
    database_url = f"postgresql://{usuario}:{senha}@{host}:{porta}/{banco}"
    
    env_content = f"""# Configuracoes do Banco de Dados Personal Agent
DATABASE_URL_PERSONAL={database_url}

# Configuracoes do Servidor MCP
MCP_PORT={mcp_port}
MCP_HOST={mcp_host}
"""
    
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print(f"[OK] Arquivo .env criado em: {env_path}")
        print("\nConfiguracoes:")
        print(f"  Host: {host}")
        print(f"  Porta: {porta}")
        print(f"  Banco: {banco}")
        print(f"  Usuario: {usuario}")
        print(f"  MCP Port: {mcp_port}")
        print(f"  MCP Host: {mcp_host}")
        print("\nIMPORTANTE: Edite o arquivo .env e configure a senha correta!")
        return True
    except Exception as e:
        print(f"[ERRO] Erro ao criar .env: {e}")
        return False


if __name__ == "__main__":
    # Valores padrão para servidor Hostinger
    if len(sys.argv) > 1:
        # Permite passar senha como argumento: python criar_env.py SENHA_AQUI
        criar_env_rapido(senha=sys.argv[1])
    else:
        # Cria com senha padrão (deve ser alterada)
        criar_env_rapido()
