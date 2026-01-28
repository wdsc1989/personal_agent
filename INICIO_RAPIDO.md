# ⚡ Início Rápido - Deploy Agente Pessoal

## 🎯 Objetivo
Subir o sistema completo no servidor Hostinger em 10 passos.

---

## 📋 Passo a Passo

### ✅ PASSO 1: Preparar Localmente

**No seu computador Windows:**

1. Edite o arquivo `.env` e configure a senha:
   ```bash
   notepad .env
   ```
   Altere: `SENHA_SEGURA_AQUI` → `SUA_SENHA_REAL`

2. Edite o script SQL e configure a senha:
   ```bash
   notepad scripts\create_personal_agent_db.sql
   ```
   Altere na linha 9: `SENHA_SEGURA_AQUI` → `SUA_SENHA_REAL`

---

### ✅ PASSO 2: Conectar ao Servidor

```bash
ssh root@srv1140258.hstgr.cloud
```

---

### ✅ PASSO 3: Criar Diretório

```bash
sudo mkdir -p /opt/personal_agent
sudo chown $USER:$USER /opt/personal_agent
cd /opt/personal_agent
```

---

### ✅ PASSO 4: Copiar Arquivos

**Opção A - Via Git:**
```bash
git clone https://seu-repositorio.git /opt/personal_agent
cd /opt/personal_agent
```

**Opção B - Via SCP (do seu PC):**
```powershell
# No PowerShell do Windows
scp -r "c:\Users\DELL\Documents\Projetos\Contabil\personal_agent\*" root@srv1140258.hstgr.cloud:/opt/personal_agent/
```

**Opção C - Via SFTP:**
Use FileZilla ou WinSCP para copiar os arquivos.

---

### ✅ PASSO 5: Criar Ambiente Virtual

```bash
cd /opt/personal_agent
python3 -m venv venv
source venv/bin/activate
```

---

### ✅ PASSO 6: Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
cd mcp_server
pip install -r requirements.txt
cd ..
```

---

### ✅ PASSO 7: Configurar .env no Servidor

```bash
nano .env
```

Configure:
```env
DATABASE_URL_PERSONAL=postgresql://personal_agent_user:SUA_SENHA_REAL@localhost:5432/personal_agent_db
MCP_PORT=8001
MCP_HOST=0.0.0.0
```

**IMPORTANTE:** Use `localhost`, não o hostname externo!

---

### ✅ PASSO 8: Criar Banco de Dados

```bash
sudo -u postgres psql -f scripts/create_personal_agent_db.sql
```

**OU manualmente:**
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
\q
```

Depois execute o restante do script SQL para criar as tabelas.

---

### ✅ PASSO 9: Inicializar Tabelas

```bash
source venv/bin/activate
python3 scripts/init_tables.py
```

---

### ✅ PASSO 10: Configurar e Iniciar Serviço

```bash
# Editar caminhos no arquivo de serviço (se necessário)
nano mcp_server/systemd/mcp-server.service

# Copiar e configurar
sudo cp mcp_server/systemd/mcp-server.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable mcp-server
sudo systemctl start mcp-server
```

---

## ✅ Verificação

```bash
# Verificar status
sudo systemctl status mcp-server

# Ver logs
sudo journalctl -u mcp-server -f

# Testar servidor
curl http://localhost:8001/health
```

---

## 🎉 Pronto!

Se tudo estiver OK, configure o n8n seguindo:
`workflows/N8N_WORKFLOW_GUIDE.md`

---

## 🆘 Problemas?

### Serviço não inicia:
```bash
sudo journalctl -u mcp-server -n 100
```

### Erro de conexão:
```bash
python3 scripts/test_connection.py
```

### Ver mais ajuda:
- `DEPLOY_COMPLETO.md` - Guia completo
- `COMANDOS_DEPLOY.txt` - Comandos prontos
- `INDEX_DOCUMENTACAO.md` - Índice completo

---

**Boa sorte! 🚀**
