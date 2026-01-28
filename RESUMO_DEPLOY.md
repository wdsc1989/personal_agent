# 📋 Resumo Rápido - Deploy Agente Pessoal

## 🎯 Objetivo
Subir o Agente Pessoal completo no servidor Hostinger (srv1140258.hstgr.cloud)

---

## ✅ Checklist Pré-Deploy

### Local (seu computador):
- [x] Estrutura do projeto criada
- [x] Arquivo `.env` criado (editar senha!)
- [x] Scripts SQL preparados
- [x] Documentação completa

### No servidor:
- [ ] Diretório `/opt/personal_agent` criado
- [ ] Arquivos copiados para o servidor
- [ ] `.env` configurado no servidor
- [ ] Dependências instaladas
- [ ] Banco de dados criado
- [ ] Tabelas inicializadas
- [ ] Serviço systemd configurado
- [ ] Serviço rodando

---

## 🚀 Passos Rápidos

### 1. Conectar ao servidor
```bash
ssh root@srv1140258.hstgr.cloud
```

### 2. Criar diretório e copiar arquivos
```bash
sudo mkdir -p /opt/personal_agent
sudo chown $USER:$USER /opt/personal_agent
cd /opt/personal_agent
# Copiar arquivos via git, scp ou sftp
```

### 3. Setup rápido (use o script)
```bash
cd /opt/personal_agent
chmod +x scripts/deploy_servidor.sh
./scripts/deploy_servidor.sh
```

### 4. OU fazer manualmente:

#### 3.1 Ambiente virtual e dependências
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd mcp_server && pip install -r requirements.txt && cd ..
```

#### 3.2 Configurar .env
```bash
nano .env
# Configure: DATABASE_URL_PERSONAL=postgresql://personal_agent_user:SENHA@localhost:5432/personal_agent_db
```

#### 3.3 Criar banco
```bash
sudo -u postgres psql -f scripts/create_personal_agent_db.sql
```

#### 3.4 Inicializar tabelas
```bash
source venv/bin/activate
python3 scripts/init_tables.py
```

#### 3.5 Configurar systemd
```bash
sudo cp mcp_server/systemd/mcp-server.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable mcp-server
sudo systemctl start mcp-server
```

### 5. Verificar
```bash
sudo systemctl status mcp-server
curl http://localhost:8001/health
```

---

## 📚 Documentação Completa

- **Guia completo:** `DEPLOY_COMPLETO.md`
- **Comandos prontos:** `COMANDOS_DEPLOY.txt`
- **Script automático:** `scripts/deploy_servidor.sh`

---

## 🔧 Comandos Essenciais

```bash
# Status
sudo systemctl status mcp-server

# Logs
sudo journalctl -u mcp-server -f

# Reiniciar
sudo systemctl restart mcp-server

# Testar
curl http://localhost:8001/health
```

---

## ⚠️ Importante

1. **Senha do banco:** Altere `SENHA_SEGURA_AQUI` no `.env` e no script SQL
2. **Caminhos:** Ajuste caminhos no arquivo systemd se necessário
3. **Porta:** Verifique se a porta 8001 está livre
4. **Firewall:** Se n8n estiver em outro servidor, abra a porta 8001

---

## 🎉 Pronto!

Após tudo funcionando, configure o n8n seguindo:
`workflows/N8N_WORKFLOW_GUIDE.md`
