#!/bin/bash
# Script completo de deploy no servidor Hostinger
# Execute no servidor após copiar os arquivos

set -e  # Para em caso de erro

echo "=========================================="
echo "DEPLOY AGENTE PESSOAL - SERVIDOR HOSTINGER"
echo "=========================================="

# Diretório de deploy
DEPLOY_DIR="/opt/personal_agent"
PYTHON_CMD="python3"

# Verificar se está no diretório correto
if [ ! -f "requirements.txt" ]; then
    echo "ERRO: Execute este script do diretório personal_agent!"
    exit 1
fi

echo ""
echo "1. Verificando diretório..."
if [ ! -d "$DEPLOY_DIR" ]; then
    echo "   Criando diretório $DEPLOY_DIR..."
    sudo mkdir -p $DEPLOY_DIR
    sudo chown $USER:$USER $DEPLOY_DIR
fi

echo ""
echo "2. Criando ambiente virtual..."
cd $DEPLOY_DIR
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
fi
source venv/bin/activate

echo ""
echo "3. Instalando dependências..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
cd mcp_server
pip install -r requirements.txt --quiet
cd ..

echo ""
echo "4. Verificando arquivo .env..."
if [ ! -f ".env" ]; then
    echo "   AVISO: Arquivo .env não encontrado!"
    echo "   Copie o .env.example para .env e configure:"
    echo "   cp .env.example .env"
    echo "   nano .env"
    read -p "   Pressione Enter após configurar o .env..."
fi

echo ""
echo "5. Criando banco de dados..."
if [ -f "scripts/create_personal_agent_db.sql" ]; then
    echo "   Executando script SQL..."
    sudo -u postgres psql -f scripts/create_personal_agent_db.sql || {
        echo "   AVISO: Erro ao executar script SQL."
        echo "   Execute manualmente: sudo -u postgres psql -f scripts/create_personal_agent_db.sql"
    }
else
    echo "   AVISO: Script SQL não encontrado!"
fi

echo ""
echo "6. Inicializando tabelas..."
$PYTHON_CMD -c "from config.database import init_db_personal; init_db_personal()" || {
    echo "   AVISO: Erro ao inicializar tabelas."
    echo "   Verifique a conexão com o banco."
}

echo ""
echo "7. Configurando systemd..."
if [ -f "mcp_server/systemd/mcp-server.service" ]; then
    # Ajustar caminhos no arquivo de serviço
    sed -i "s|WorkingDirectory=.*|WorkingDirectory=$DEPLOY_DIR/mcp_server|g" mcp_server/systemd/mcp-server.service
    sed -i "s|ExecStart=.*|ExecStart=$DEPLOY_DIR/venv/bin/python3 $DEPLOY_DIR/mcp_server/main.py|g" mcp_server/systemd/mcp-server.service
    
    sudo cp mcp_server/systemd/mcp-server.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable mcp-server
    echo "   Serviço configurado!"
else
    echo "   AVISO: Arquivo de serviço não encontrado!"
fi

echo ""
echo "8. Iniciando serviço..."
sudo systemctl start mcp-server || {
    echo "   AVISO: Erro ao iniciar serviço."
    echo "   Verifique os logs: sudo journalctl -u mcp-server -n 50"
}

echo ""
echo "9. Verificando status..."
sleep 2
sudo systemctl status mcp-server --no-pager -l || true

echo ""
echo "=========================================="
echo "DEPLOY CONCLUÍDO!"
echo "=========================================="
echo ""
echo "Comandos úteis:"
echo "  Ver logs: sudo journalctl -u mcp-server -f"
echo "  Testar: curl http://localhost:8001/health"
echo "  Status: sudo systemctl status mcp-server"
echo "  Reiniciar: sudo systemctl restart mcp-server"
echo ""
