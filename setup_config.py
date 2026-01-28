"""
Script interativo para configurar o Agente Pessoal
"""
import os
import sys
from pathlib import Path
import secrets

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def criar_env():
    """Cria arquivo .env com configurações"""
    env_path = Path(__file__).parent / '.env'
    
    if env_path.exists():
        resposta = input("[AVISO] Arquivo .env ja existe. Deseja sobrescrever? (s/N): ")
        if resposta.lower() != 's':
            print("[ERRO] Operacao cancelada.")
            return False
    
    print("\n" + "="*60)
    print("CONFIGURACAO DO AGENTE PESSOAL")
    print("="*60 + "\n")
    
    # Informações do banco de dados
    print("CONFIGURACAO DO BANCO DE DADOS")
    print("-" * 60)
    
    # Host do banco
    print("\n1. Onde esta o banco de dados PostgreSQL?")
    print("   [1] Local (localhost)")
    print("   [2] Servidor Hostinger (srv1140258.hstgr.cloud)")
    print("   [3] Outro")
    
    opcao_host = input("\nEscolha uma opcao (1-3): ").strip()
    
    if opcao_host == "1":
        db_host = "localhost"
    elif opcao_host == "2":
        db_host = "srv1140258.hstgr.cloud"
    else:
        db_host = input("Digite o host do banco: ").strip()
    
    # Porta
    db_port = input("\n2. Porta do PostgreSQL (padrao: 5432): ").strip() or "5432"
    
    # Nome do banco
    db_name = input("3. Nome do banco de dados (padrao: personal_agent_db): ").strip() or "personal_agent_db"
    
    # Usuário
    db_user = input("4. Usuario do banco (padrao: personal_agent_user): ").strip() or "personal_agent_user"
    
    # Senha
    print("\n5. Senha do banco de dados:")
    db_password = input("   Digite a senha: ").strip()
    
    if not db_password:
        print("[AVISO] Senha vazia! Configure uma senha segura.")
        db_password = "SENHA_SEGURA_AQUI"
    
    # URL do banco
    database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    # Configurações do servidor MCP
    print("\n" + "="*60)
    print("CONFIGURACAO DO SERVIDOR MCP")
    print("-" * 60)
    
    mcp_port = input("\n1. Porta do servidor MCP (padrao: 8001): ").strip() or "8001"
    mcp_host = input("2. Host do servidor MCP (padrao: 0.0.0.0): ").strip() or "0.0.0.0"
    
    # Criar conteúdo do .env
    env_content = f"""# Configurações do Banco de Dados Personal Agent
DATABASE_URL_PERSONAL={database_url}

# Configurações do Servidor MCP
MCP_PORT={mcp_port}
MCP_HOST={mcp_host}
"""
    
    # Salvar arquivo
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("\n" + "="*60)
        print("[OK] Arquivo .env criado com sucesso!")
        print("="*60)
        print(f"\nLocalizacao: {env_path}")
        print("\nConfiguracoes salvas:")
        print(f"   - Host: {db_host}")
        print(f"   - Porta: {db_port}")
        print(f"   - Banco: {db_name}")
        print(f"   - Usuario: {db_user}")
        print(f"   - MCP Port: {mcp_port}")
        print(f"   - MCP Host: {mcp_host}")
        
        return True
        
    except Exception as e:
        print(f"\n[ERRO] Erro ao criar arquivo .env: {e}")
        return False


def testar_conexao():
    """Testa conexão com o banco de dados"""
    print("\n" + "="*60)
    print("TESTANDO CONEXAO COM O BANCO")
    print("="*60 + "\n")
    
    try:
        from config.database import test_connection_personal
        if test_connection_personal():
            print("\n[OK] Conexao estabelecida com sucesso!")
            return True
        else:
            print("\n[ERRO] Falha na conexao. Verifique as credenciais.")
            return False
    except Exception as e:
        print(f"\n[ERRO] Erro ao testar conexao: {e}")
        return False


def inicializar_banco():
    """Inicializa as tabelas do banco"""
    print("\n" + "="*60)
    print("INICIALIZANDO BANCO DE DADOS")
    print("="*60 + "\n")
    
    try:
        from config.database import init_db_personal
        init_db_personal()
        print("\n[OK] Tabelas criadas com sucesso!")
        return True
    except Exception as e:
        print(f"\n[ERRO] Erro ao inicializar banco: {e}")
        return False


def main():
    """Função principal"""
    print("\n" + "="*60)
    print("AGENTE PESSOAL - CONFIGURACAO INICIAL")
    print("="*60 + "\n")
    
    # Passo 1: Criar .env
    if not criar_env():
        return
    
    # Passo 2: Testar conexão
    print("\n" + "-"*60)
    resposta = input("Deseja testar a conexao agora? (S/n): ").strip()
    if resposta.lower() != 'n':
        if not testar_conexao():
            print("\n[AVISO] A conexao falhou. Verifique:")
            print("   1. Se o PostgreSQL esta rodando")
            print("   2. Se as credenciais estao corretas")
            print("   3. Se o banco de dados foi criado")
            print("\nDica: Execute o script SQL primeiro:")
            print("   psql -U postgres -f scripts/create_personal_agent_db.sql")
            return
    
    # Passo 3: Inicializar banco
    print("\n" + "-"*60)
    resposta = input("Deseja criar as tabelas agora? (S/n): ").strip()
    if resposta.lower() != 'n':
        inicializar_banco()
    
    # Resumo
    print("\n" + "="*60)
    print("[OK] CONFIGURACAO CONCLUIDA!")
    print("="*60)
    print("\nProximos passos:")
    print("   1. Instale as dependencias: pip install -r requirements.txt")
    print("   2. Instale dependencias do MCP: cd mcp_server && pip install -r requirements.txt")
    print("   3. Inicie o servidor MCP: cd mcp_server && python main.py")
    print("   4. Configure o fluxo n8n seguindo: workflows/N8N_WORKFLOW_GUIDE.md")
    print("\nDocumentacao completa em: docs/MVP_AGENTE_PESSOAL.md")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
