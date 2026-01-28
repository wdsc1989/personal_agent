#!/bin/bash
# Script completo de deploy automático no servidor Hostinger
# Execute este script no servidor após fazer git clone

set -e  # Para em caso de erro

echo "============================================================"
echo "  DEPLOY AUTOMATICO - AGENTE PESSOAL"
echo "  Servidor: srv1140258.hstgr.cloud"
echo "============================================================"
echo ""

# Configurações
DEPLOY_DIR="/opt/personal_agent"
PYTHON_CMD="python3"
REPO_URL="https://github.com/wdsc1989/personal_agent.git"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para imprimir mensagens
print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

# Função para codificar senha para URL (URL encode)
url_encode() {
    local string="${1}"
    local strlen=${#string}
    local encoded=""
    local pos c o

    for (( pos=0 ; pos<strlen ; pos++ )); do
        c=${string:$pos:1}
        case "$c" in
            [-_.~a-zA-Z0-9] ) o="${c}" ;;
            * ) printf -v o '%%%02x' "'$c" ;;
        esac
        encoded+="${o}"
    done
    echo "${encoded}"
}

# Função para codificar senha para URL (necessário se senha contém caracteres especiais)
urlencode() {
    local string="${1}"
    local strlen=${#string}
    local encoded=""
    local pos c o

    for (( pos=0 ; pos<strlen ; pos++ )); do
        c=${string:$pos:1}
        case "$c" in
            [-_.~a-zA-Z0-9] ) o="${c}" ;;
            * ) printf -v o '%%%02x' "'$c"
        esac
        encoded+="${o}"
    done
    echo "${encoded}"
}

# Verificar se está rodando como root ou com sudo
if [ "$EUID" -ne 0 ]; then 
    print_info "Alguns comandos precisam de sudo. Você será solicitado a inserir a senha."
fi

# PASSO 1: Verificar/Criar diretório
echo ""
echo "============================================================"
echo "PASSO 1: Preparando diretório"
echo "============================================================"

if [ -d "$DEPLOY_DIR" ]; then
    print_info "Diretório $DEPLOY_DIR já existe"
    read -p "Deseja continuar e atualizar? (s/N): " resposta
    if [ "$resposta" != "s" ] && [ "$resposta" != "S" ]; then
        print_error "Deploy cancelado"
        exit 1
    fi
    cd $DEPLOY_DIR
    if [ -d ".git" ]; then
        print_info "Atualizando repositório Git..."
        git pull || print_error "Erro ao atualizar. Continuando..."
    fi
else
    print_info "Criando diretório $DEPLOY_DIR..."
    sudo mkdir -p $DEPLOY_DIR
    sudo chown $USER:$USER $DEPLOY_DIR
    cd $DEPLOY_DIR
    
    print_info "Clonando repositório..."
    git clone $REPO_URL . || {
        print_error "Erro ao clonar repositório. Verifique:"
        print_error "  1. Chave SSH configurada"
        print_error "  2. Acesso ao repositório"
        exit 1
    }
    print_success "Repositório clonado"
fi

# PASSO 2: Criar ambiente virtual
echo ""
echo "============================================================"
echo "PASSO 2: Configurando ambiente Python"
echo "============================================================"

cd $DEPLOY_DIR

if [ ! -d "venv" ]; then
    print_info "Criando ambiente virtual..."
    $PYTHON_CMD -m venv venv
    print_success "Ambiente virtual criado"
else
    print_info "Ambiente virtual já existe"
fi

print_info "Ativando ambiente virtual..."
source venv/bin/activate

print_info "Atualizando pip..."
pip install --upgrade pip --quiet

# PASSO 3: Instalar dependências
echo ""
echo "============================================================"
echo "PASSO 3: Instalando dependências"
echo "============================================================"

print_info "Instalando dependências principais..."
pip install -r requirements.txt --quiet || {
    print_error "Erro ao instalar dependências principais"
    exit 1
}
print_success "Dependências principais instaladas"

print_info "Instalando dependências do MCP server..."
cd mcp_server
pip install -r requirements.txt --quiet || {
    print_error "Erro ao instalar dependências do MCP"
    exit 1
}
print_success "Dependências do MCP instaladas"
cd ..

# PASSO 4: Configurar .env
echo ""
echo "============================================================"
echo "PASSO 4: Configurando arquivo .env"
echo "============================================================"

if [ ! -f ".env" ]; then
    print_info "Arquivo .env não encontrado. Criando a partir do exemplo..."
    cp .env.example .env
    
    print_error "============================================================"
    print_error "ATENCAO: Configure a senha do banco de dados!"
    print_error "============================================================"
    echo ""
    read -p "Digite a senha do banco de dados: " -s DB_PASSWORD
    echo ""
    
    # Codificar senha para URL (necessário se contém caracteres especiais como @)
    DB_PASSWORD_ENCODED=$(url_encode "$DB_PASSWORD")
    
    # Atualizar .env com a senha codificada
    sed -i "s|SENHA_SEGURA_AQUI|$DB_PASSWORD_ENCODED|g" .env
    sed -i "s|localhost|localhost|g" .env  # Garantir que usa localhost
    
    print_success "Arquivo .env configurado"
else
    print_info "Arquivo .env já existe"
    read -p "Deseja reconfigurar a senha? (s/N): " resposta
    if [ "$resposta" = "s" ] || [ "$resposta" = "S" ]; then
        read -p "Digite a senha do banco de dados: " -s DB_PASSWORD
        echo ""
        
        # Codificar senha para URL
        DB_PASSWORD_ENCODED=$(url_encode "$DB_PASSWORD")
        
        sed -i "s|SENHA_SEGURA_AQUI|$DB_PASSWORD_ENCODED|g" .env
        # Atualizar senha existente na URL (usando senha codificada)
        sed -i "s|postgresql://personal_agent_user:[^@]*@|postgresql://personal_agent_user:$DB_PASSWORD_ENCODED@|g" .env
        print_success "Senha atualizada no .env"
    fi
fi

# PASSO 5: Criar banco de dados
echo ""
echo "============================================================"
echo "PASSO 5: Criando banco de dados"
echo "============================================================"

# Verificar se banco já existe
DB_EXISTS=$(sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='personal_agent_db'" 2>/dev/null || echo "0")

if [ "$DB_EXISTS" = "1" ]; then
    print_info "Banco de dados personal_agent_db já existe"
    read -p "Deseja recriar? Isso apagará todos os dados! (s/N): " resposta
    if [ "$resposta" = "s" ] || [ "$resposta" = "S" ]; then
        print_info "Removendo banco existente..."
        sudo -u postgres psql -c "DROP DATABASE IF EXISTS personal_agent_db;" 2>/dev/null || true
        sudo -u postgres psql -c "DROP USER IF EXISTS personal_agent_user;" 2>/dev/null || true
    else
        print_info "Mantendo banco existente. Pulando criação..."
        SKIP_DB_CREATE=true
    fi
fi

if [ "$SKIP_DB_CREATE" != "true" ]; then
    print_info "Criando banco de dados e usuário..."
    
    # Ler senha do .env (pode estar codificada, vamos usar a original)
    # Primeiro tenta ler a senha que foi digitada (não codificada)
    if [ -z "$DB_PASSWORD" ]; then
        # Se não tiver a variável, tenta decodificar da URL
        DB_PASSWORD_RAW=$(grep DATABASE_URL_PERSONAL .env | sed 's/.*:\/\/[^:]*:\([^@]*\)@.*/\1/')
        # Decodificar URL (substituir %40 por @, etc)
        DB_PASSWORD=$(echo "$DB_PASSWORD_RAW" | sed 's/%40/@/g' | sed 's/%21/!/g' | sed 's/%23/#/g' | sed 's/%24/$/g' | sed 's/%25/%/g' | sed 's/%26/\&/g' | sed 's/%2B/+/g' | sed 's/%2C/,/g' | sed 's/%2F/\//g' | sed 's/%3A/:/g' | sed 's/%3B/;/g' | sed 's/%3D/=/g' | sed 's/%3F/?/g')
    fi
    
    # Criar banco e usuário
    sudo -u postgres psql << EOF
-- Criar banco
CREATE DATABASE personal_agent_db;

-- Criar usuário
CREATE USER personal_agent_user WITH PASSWORD '$DB_PASSWORD';

-- Dar permissões
GRANT ALL PRIVILEGES ON DATABASE personal_agent_db TO personal_agent_user;
EOF
    
    # Conectar ao banco e dar permissões no schema
    sudo -u postgres psql -d personal_agent_db << EOF
-- Dar permissões no schema
GRANT ALL ON SCHEMA public TO personal_agent_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO personal_agent_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO personal_agent_user;
EOF
    
    if [ $? -ne 0 ]; then
        print_error "Erro ao criar banco de dados"
        exit 1
    fi
    
    print_success "Banco de dados criado"
    
    # Criar tabelas usando o script SQL
    print_info "Criando tabelas..."
    sudo -u postgres psql -d personal_agent_db -f scripts/create_personal_agent_db.sql > /dev/null 2>&1 || {
        print_info "Script SQL completo. Tabelas serão criadas via Python..."
    }
fi

# PASSO 6: Inicializar tabelas via Python
echo ""
echo "============================================================"
echo "PASSO 6: Inicializando tabelas"
echo "============================================================"

print_info "Testando conexão..."
source venv/bin/activate
python3 scripts/test_connection.py && {
    print_success "Conexão OK"
    
    print_info "Criando tabelas..."
    python3 scripts/init_tables.py && {
        print_success "Tabelas criadas/verificadas"
    } || {
        print_error "Erro ao criar tabelas. Verifique os logs acima."
    }
} || {
    print_error "Erro na conexão. Verifique:"
    print_error "  1. PostgreSQL está rodando"
    print_error "  2. Credenciais no .env estão corretas"
    print_error "  3. Banco de dados foi criado"
    exit 1
}

# PASSO 7: Configurar systemd
echo ""
echo "============================================================"
echo "PASSO 7: Configurando serviço systemd"
echo "============================================================"

print_info "Ajustando arquivo de serviço..."
# Ajustar caminhos no arquivo de serviço
sed -i "s|WorkingDirectory=.*|WorkingDirectory=$DEPLOY_DIR/mcp_server|g" mcp_server/systemd/mcp-server.service
sed -i "s|ExecStart=.*|ExecStart=$DEPLOY_DIR/venv/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8001|g" mcp_server/systemd/mcp-server.service
sed -i "s|Environment=.*|Environment=\"PATH=$DEPLOY_DIR/venv/bin:/usr/bin:/usr/local/bin\"|g" mcp_server/systemd/mcp-server.service

print_info "Copiando arquivo de serviço..."
sudo cp mcp_server/systemd/mcp-server.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable mcp-server
print_success "Serviço configurado e habilitado"

# PASSO 8: Iniciar serviço
echo ""
echo "============================================================"
echo "PASSO 8: Iniciando serviço"
echo "============================================================"

print_info "Parando serviço se estiver rodando..."
sudo systemctl stop mcp-server 2>/dev/null || true

print_info "Iniciando serviço..."
sudo systemctl start mcp-server

sleep 3

# Verificar status
if sudo systemctl is-active --quiet mcp-server; then
    print_success "Serviço iniciado com sucesso!"
else
    print_error "Serviço não iniciou. Verificando logs..."
    sudo journalctl -u mcp-server -n 20 --no-pager
    exit 1
fi

# PASSO 9: Verificação final
echo ""
echo "============================================================"
echo "PASSO 9: Verificação final"
echo "============================================================"

print_info "Verificando status do serviço..."
sudo systemctl status mcp-server --no-pager -l | head -n 10

print_info "Testando endpoint de health..."
sleep 2
if curl -s http://localhost:8001/health > /dev/null 2>&1; then
    print_success "Servidor MCP respondendo!"
else
    print_error "Servidor não está respondendo. Verifique os logs:"
    print_info "sudo journalctl -u mcp-server -f"
fi

# Resumo final
echo ""
echo "============================================================"
echo "  DEPLOY CONCLUIDO COM SUCESSO!"
echo "============================================================"
echo ""
echo "Informacoes:"
echo "  - Diretorio: $DEPLOY_DIR"
echo "  - Servidor MCP: http://localhost:8001"
echo "  - Status: $(sudo systemctl is-active mcp-server)"
echo ""
echo "Comandos uteis:"
echo "  Ver logs:     sudo journalctl -u mcp-server -f"
echo "  Status:        sudo systemctl status mcp-server"
echo "  Reiniciar:     sudo systemctl restart mcp-server"
echo "  Parar:         sudo systemctl stop mcp-server"
echo "  Testar:        curl http://localhost:8001/health"
echo ""
echo "Proximo passo:"
echo "  Configure o fluxo n8n seguindo: workflows/N8N_WORKFLOW_GUIDE.md"
echo ""
echo "============================================================"
