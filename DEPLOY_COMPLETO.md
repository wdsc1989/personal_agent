# 🚀 Guia Completo de Deploy - Agente Pessoal

Este guia cobre todos os passos desde a configuração local até o deploy no servidor Hostinger.

---

## 📋 Índice

1. [Preparação Local](#1-preparação-local)
2. [Configuração do Banco de Dados](#2-configuração-do-banco-de-dados)
3. [Testes Locais](#3-testes-locais)
4. [Preparação para Deploy](#4-preparação-para-deploy)
5. [Deploy no Servidor](#5-deploy-no-servidor)
6. [Configuração no Servidor](#6-configuração-no-servidor)
7. [Verificação Final](#7-verificação-final)

---

## 1. Preparação Local

### 1.1 Verificar estrutura do projeto

```bash
cd c:\Users\DELL\Documents\Projetos\Contabil\personal_agent
dir
```

Certifique-se de que todos os diretórios existem:
- `config/`
- `models/`
- `services/`
- `mcp_server/`
- `scripts/`
- `workflows/`
- `docs/`

### 1.2 Configurar arquivo .env

O arquivo `.env` já foi criado. **Edite e configure a senha:**

```bash
notepad .env
```

Altere:
```env
DATABASE_URL_PERSONAL=postgresql://personal_agent_user:SUA_SENHA_REAL@srv1140258.hstgr.cloud:5432/personal_agent_db
```

### 1.3 Instalar dependências localmente (opcional, para testes)

```bash
pip install -r requirements.txt
cd mcp_server
pip install -r requirements.txt
cd ..
```

---

## 2. Configuração do Banco de Dados

### 2.1 Preparar script SQL

Edite o arquivo `scripts/create_personal_agent_db.sql` e altere a senha:

```sql
-- Linha 9: Altere a senha
CREATE USER personal_agent_user WITH PASSWORD 'SUA_SENHA_REAL_AQUI';
```

### 2.2 Criar script de deploy SQL

Crie um arquivo `scripts/deploy_db.sh` para facilitar:

```bash
#!/bin/bash
# Script para criar banco de dados no servidor

echo "Criando banco de dados personal_agent_db..."

sudo -u postgres psql << EOF
-- Criar banco
CREATE DATABASE personal_agent_db;

-- Criar usuário
CREATE USER personal_agent_user WITH PASSWORD 'SUA_SENHA_REAL_AQUI';

-- Dar permissões
GRANT ALL PRIVILEGES ON DATABASE personal_agent_db TO personal_agent_user;

-- Conectar ao banco
\c personal_agent_db

-- Dar permissões no schema
GRANT ALL ON SCHEMA public TO personal_agent_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO personal_agent_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO personal_agent_user;
EOF

echo "Banco criado! Agora execute o restante do script SQL..."
```

---

## 3. Testes Locais

### 3.1 Testar conexão (se tiver acesso ao servidor)

```python
# test_connection.py
from config.database import test_connection_personal, init_db_personal

print("Testando conexão...")
if test_connection_personal():
    print("Conexão OK! Inicializando tabelas...")
    init_db_personal()
    print("Tabelas criadas!")
else:
    print("Erro na conexão. Verifique as credenciais.")
```

Execute:
```bash
python test_connection.py
```

### 3.2 Testar servidor MCP localmente (se possível)

```bash
cd mcp_server
python main.py
```

Em outro terminal:
```bash
curl http://localhost:8001/health
```

---

## 4. Preparação para Deploy

### 4.1 Criar arquivo de comandos para o servidor

Crie `scripts/deploy_servidor.sh`:

```bash
#!/bin/bash
# Script completo de deploy no servidor Hostinger

set -e  # Para em caso de erro

echo "=========================================="
echo "DEPLOY AGENTE PESSOAL - SERVIDOR HOSTINGER"
echo "=========================================="

# Diretório de destino no servidor
DEPLOY_DIR="/opt/personal_agent"
PYTHON_CMD="python3"

echo ""
echo "1. Criando diretório de deploy..."
sudo mkdir -p $DEPLOY_DIR
sudo chown $USER:$USER $DEPLOY_DIR

echo ""
echo "2. Copiando arquivos..."
# Os arquivos serão copiados via git ou scp

echo ""
echo "3. Criando ambiente virtual (recomendado)..."
cd $DEPLOY_DIR
$PYTHON_CMD -m venv venv
source venv/bin/activate

echo ""
echo "4. Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt
cd mcp_server
pip install -r requirements.txt
cd ..

echo ""
echo "5. Configurando arquivo .env..."
# O arquivo .env deve ser criado manualmente ou copiado

echo ""
echo "6. Criando banco de dados..."
sudo -u postgres psql -f scripts/create_personal_agent_db.sql

echo ""
echo "7. Inicializando tabelas..."
$PYTHON_CMD -c "from config.database import init_db_personal; init_db_personal()"

echo ""
echo "8. Configurando systemd..."
sudo cp mcp_server/systemd/mcp-server.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable mcp-server

echo ""
echo "9. Iniciando serviço..."
sudo systemctl start mcp-server

echo ""
echo "10. Verificando status..."
sudo systemctl status mcp-server --no-pager

echo ""
echo "=========================================="
echo "DEPLOY CONCLUÍDO!"
echo "=========================================="
echo ""
echo "Verificar logs: sudo journalctl -u mcp-server -f"
echo "Testar servidor: curl http://localhost:8001/health"
```

### 4.2 Criar checklist de deploy

Crie `CHECKLIST_DEPLOY.md`:

```markdown
# ✅ Checklist de Deploy

## Antes de fazer deploy:

- [ ] Arquivo .env configurado com senha real
- [ ] Script SQL editado com senha real
- [ ] Dependências testadas localmente
- [ ] Código commitado no git (se usar)
- [ ] Backup do banco atual (se existir)

## No servidor:

- [ ] Diretório criado (/opt/personal_agent)
- [ ] Arquivos copiados
- [ ] .env configurado no servidor
- [ ] Dependências instaladas
- [ ] Banco de dados criado
- [ ] Tabelas inicializadas
- [ ] Serviço systemd configurado
- [ ] Serviço iniciado e rodando
- [ ] Testes de conexão OK
- [ ] Servidor MCP respondendo
```

---

## 5. Deploy no Servidor

### 5.1 Conectar ao servidor

```bash
ssh root@srv1140258.hstgr.cloud
# ou
ssh seu_usuario@srv1140258.hstgr.cloud
```

### 5.2 Criar diretório de deploy

```bash
sudo mkdir -p /opt/personal_agent
sudo chown $USER:$USER /opt/personal_agent
cd /opt/personal_agent
```

### 5.3 Copiar arquivos

**Opção A: Via Git (recomendado)**

```bash
# Se o projeto estiver em um repositório git
git clone https://seu-repositorio.git /opt/personal_agent
cd /opt/personal_agent
```

**Opção B: Via SCP (do seu computador local)**

No seu computador Windows:
```powershell
# Instalar WinSCP ou usar PowerShell com scp
scp -r "c:\Users\DELL\Documents\Projetos\Contabil\personal_agent\*" root@srv1140258.hstgr.cloud:/opt/personal_agent/
```

**Opção C: Manual (copiar arquivo por arquivo)**

Use um cliente SFTP como FileZilla ou WinSCP.

### 5.4 Criar ambiente virtual (recomendado)

```bash
cd /opt/personal_agent
python3 -m venv venv
source venv/bin/activate
```

---

## 6. Configuração no Servidor

### 6.1 Instalar dependências

```bash
cd /opt/personal_agent
source venv/bin/activate  # Se usar venv

# Atualizar pip
pip install --upgrade pip

# Instalar dependências principais
pip install -r requirements.txt

# Instalar dependências do MCP
cd mcp_server
pip install -r requirements.txt
cd ..
```

### 6.2 Configurar arquivo .env no servidor

```bash
cd /opt/personal_agent
nano .env
```

Configure:
```env
DATABASE_URL_PERSONAL=postgresql://personal_agent_user:SUA_SENHA_REAL@localhost:5432/personal_agent_db
MCP_PORT=8001
MCP_HOST=0.0.0.0
```

**IMPORTANTE:** Use `localhost` no servidor, não o hostname externo!

### 6.3 Criar banco de dados

```bash
cd /opt/personal_agent

# Editar script SQL primeiro (alterar senha)
nano scripts/create_personal_agent_db.sql

# Executar script
sudo -u postgres psql -f scripts/create_personal_agent_db.sql
```

Ou execute manualmente:

```bash
sudo -u postgres psql
```

No psql:
```sql
CREATE DATABASE personal_agent_db;
CREATE USER personal_agent_user WITH PASSWORD 'SUA_SENHA_REAL';
GRANT ALL PRIVILEGES ON DATABASE personal_agent_db TO personal_agent_user;
\c personal_agent_db
GRANT ALL ON SCHEMA public TO personal_agent_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO personal_agent_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO personal_agent_user;

-- Agora execute o restante do script SQL para criar as tabelas
\i scripts/create_personal_agent_db.sql
```

### 6.4 Inicializar tabelas

```bash
cd /opt/personal_agent
source venv/bin/activate  # Se usar venv
python3 -c "from config.database import init_db_personal; init_db_personal()"
```

Ou crie um script:

```bash
# init_tables.py
from config.database import init_db_personal, test_connection_personal

print("Testando conexão...")
if test_connection_personal():
    print("Conexão OK!")
    print("Inicializando tabelas...")
    init_db_personal()
    print("Tabelas criadas com sucesso!")
else:
    print("ERRO: Não foi possível conectar ao banco!")
```

Execute:
```bash
python3 init_tables.py
```

### 6.5 Configurar serviço systemd

```bash
cd /opt/personal_agent

# Editar arquivo de serviço (ajustar caminhos se necessário)
nano mcp_server/systemd/mcp-server.service
```

Verifique e ajuste:
- `WorkingDirectory=/opt/personal_agent/mcp_server`
- `ExecStart=/opt/personal_agent/venv/bin/python3 /opt/personal_agent/mcp_server/main.py` (se usar venv)
- Ou: `ExecStart=/usr/bin/python3 /opt/personal_agent/mcp_server/main.py`

Copiar e configurar:
```bash
sudo cp mcp_server/systemd/mcp-server.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable mcp-server
```

### 6.6 Iniciar serviço

```bash
sudo systemctl start mcp-server
sudo systemctl status mcp-server
```

---

## 7. Verificação Final

### 7.1 Verificar serviço

```bash
sudo systemctl status mcp-server
```

Deve mostrar: `Active: active (running)`

### 7.2 Verificar logs

```bash
sudo journalctl -u mcp-server -n 50 --no-pager
```

### 7.3 Testar servidor MCP

```bash
curl http://localhost:8001/health
```

Ou:
```bash
curl http://localhost:8001/
```

### 7.4 Testar endpoints

```bash
# Testar detecção
curl -X POST http://localhost:8001/mcp/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "adicionar conta teste", "context": {}}'
```

### 7.5 Verificar banco de dados

```bash
sudo -u postgres psql -d personal_agent_db -c "\dt"
```

Deve mostrar as tabelas:
- `usuarios_telegram`
- `contas_pagar`

### 7.6 Testar conexão Python

```bash
cd /opt/personal_agent
source venv/bin/activate
python3 -c "from config.database import test_connection_personal; test_connection_personal()"
```

---

## 🔧 Comandos Úteis

### Gerenciar serviço

```bash
# Iniciar
sudo systemctl start mcp-server

# Parar
sudo systemctl stop mcp-server

# Reiniciar
sudo systemctl restart mcp-server

# Status
sudo systemctl status mcp-server

# Habilitar no boot
sudo systemctl enable mcp-server

# Desabilitar no boot
sudo systemctl disable mcp-server
```

### Ver logs

```bash
# Últimas 50 linhas
sudo journalctl -u mcp-server -n 50

# Seguir logs em tempo real
sudo journalctl -u mcp-server -f

# Logs desde hoje
sudo journalctl -u mcp-server --since today
```

### Testar conexão banco

```bash
psql -U personal_agent_user -d personal_agent_db -h localhost
```

### Verificar porta

```bash
sudo netstat -tlnp | grep 8001
# ou
sudo ss -tlnp | grep 8001
```

---

## 🆘 Troubleshooting

### Serviço não inicia

1. Verificar logs:
   ```bash
   sudo journalctl -u mcp-server -n 100
   ```

2. Verificar arquivo .env:
   ```bash
   cat /opt/personal_agent/.env
   ```

3. Testar manualmente:
   ```bash
   cd /opt/personal_agent/mcp_server
   python3 main.py
   ```

### Erro de conexão com banco

1. Verificar se PostgreSQL está rodando:
   ```bash
   sudo systemctl status postgresql
   ```

2. Verificar se banco existe:
   ```bash
   sudo -u postgres psql -l | grep personal_agent_db
   ```

3. Testar conexão:
   ```bash
   psql -U personal_agent_user -d personal_agent_db -h localhost
   ```

### Porta já em uso

1. Verificar o que está usando a porta:
   ```bash
   sudo lsof -i :8001
   ```

2. Alterar porta no .env e reiniciar serviço

---

## ✅ Checklist Final

- [ ] Servidor MCP rodando
- [ ] Endpoint /health respondendo
- [ ] Banco de dados criado
- [ ] Tabelas criadas
- [ ] Conexão testada e funcionando
- [ ] Logs sem erros
- [ ] Serviço configurado para iniciar no boot
- [ ] Pronto para configurar n8n

---

## 📱 Próximo Passo: Configurar n8n

Após tudo funcionando, configure o fluxo n8n seguindo:
- `workflows/N8N_WORKFLOW_GUIDE.md`

**URL do servidor MCP no n8n:**
- Se n8n estiver no mesmo servidor: `http://localhost:8001`
- Se n8n estiver em outro lugar: `http://srv1140258.hstgr.cloud:8001` (se porta estiver aberta)

---

**Deploy completo! 🎉**
