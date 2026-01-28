# 🚀 Próximos Passos - Configuração do Agente Pessoal

## ✅ Passo 1: Arquivo .env criado

O arquivo `.env` foi criado com as configurações padrão para o servidor Hostinger.

### ⚠️ IMPORTANTE: Editar a senha

Abra o arquivo `.env` e altere a senha:

```bash
# Edite o arquivo
nano .env
# ou
notepad .env
```

Substitua `SENHA_SEGURA_AQUI` pela senha real do banco de dados.

---

## 📋 Passo 2: Criar banco de dados no PostgreSQL

### No servidor Hostinger (srv1140258.hstgr.cloud):

1. **Conecte-se ao servidor via SSH**

2. **Edite o script SQL primeiro** (importante!):
   ```bash
   nano scripts/create_personal_agent_db.sql
   ```
   
   Altere `SENHA_SEGURA_AQUI` para uma senha real e segura.

3. **Execute o script SQL**:
   ```bash
   sudo -u postgres psql -f scripts/create_personal_agent_db.sql
   ```
   
   Ou execute manualmente:
   ```bash
   sudo -u postgres psql
   ```
   
   Depois no psql:
   ```sql
   CREATE DATABASE personal_agent_db;
   CREATE USER personal_agent_user WITH PASSWORD 'SUA_SENHA_AQUI';
   GRANT ALL PRIVILEGES ON DATABASE personal_agent_db TO personal_agent_user;
   \c personal_agent_db
   GRANT ALL ON SCHEMA public TO personal_agent_user;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO personal_agent_user;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO personal_agent_user;
   ```

4. **Criar as tabelas** (execute o restante do script SQL ou use Python):
   ```bash
   # No servidor, após criar o banco
   cd /caminho/para/personal_agent
   python3 -c "from config.database import init_db_personal; init_db_personal()"
   ```

---

## 📦 Passo 3: Instalar dependências

### No servidor Hostinger:

```bash
cd /caminho/para/personal_agent

# Dependências principais
pip3 install -r requirements.txt

# Dependências do servidor MCP
cd mcp_server
pip3 install -r requirements.txt
```

**Dependências necessárias:**
- sqlalchemy
- psycopg2-binary
- python-dotenv
- pydantic
- fastapi
- uvicorn

---

## 🧪 Passo 4: Testar conexão

```python
# No servidor
cd /caminho/para/personal_agent
python3 -c "from config.database import test_connection_personal; test_connection_personal()"
```

Se der erro, verifique:
- ✅ PostgreSQL está rodando
- ✅ Credenciais no `.env` estão corretas
- ✅ Banco `personal_agent_db` foi criado
- ✅ Usuário `personal_agent_user` tem permissões

---

## 🚀 Passo 5: Iniciar servidor MCP

### Desenvolvimento (teste):

```bash
cd /caminho/para/personal_agent/mcp_server
python3 main.py
```

O servidor estará em: `http://localhost:8001`

### Produção (systemd):

```bash
# Copiar arquivo de serviço
sudo cp mcp_server/systemd/mcp-server.service /etc/systemd/system/

# Editar caminhos no arquivo de serviço (se necessário)
sudo nano /etc/systemd/system/mcp-server.service

# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar serviço
sudo systemctl enable mcp-server

# Iniciar serviço
sudo systemctl start mcp-server

# Verificar status
sudo systemctl status mcp-server

# Ver logs
sudo journalctl -u mcp-server -f
```

---

## ✅ Passo 6: Verificar servidor MCP

```bash
# Testar endpoint de health
curl http://localhost:8001/health

# Ou acesse no navegador
# http://localhost:8001
```

---

## 📱 Passo 7: Configurar fluxo n8n

Siga o guia completo em: `workflows/N8N_WORKFLOW_GUIDE.md`

**Pontos importantes:**
- URL do servidor MCP: `http://localhost:8001` (se n8n estiver no mesmo servidor)
- Ou use o IP interno do servidor
- Configure as credenciais do Telegram Bot
- Configure as credenciais do PostgreSQL no n8n

---

## 🔍 Checklist de Verificação

- [ ] Arquivo `.env` criado e senha configurada
- [ ] Banco de dados `personal_agent_db` criado
- [ ] Usuário `personal_agent_user` criado com permissões
- [ ] Tabelas criadas (`usuarios_telegram`, `contas_pagar`)
- [ ] Dependências Python instaladas
- [ ] Conexão com banco testada e funcionando
- [ ] Servidor MCP iniciado e respondendo
- [ ] Fluxo n8n configurado
- [ ] Teste via Telegram funcionando

---

## 🆘 Troubleshooting

### Erro de conexão com banco

1. Verifique se PostgreSQL está rodando:
   ```bash
   sudo systemctl status postgresql
   ```

2. Verifique se o banco existe:
   ```bash
   sudo -u postgres psql -l | grep personal_agent_db
   ```

3. Teste conexão manual:
   ```bash
   psql -U personal_agent_user -d personal_agent_db -h localhost
   ```

### Servidor MCP não inicia

1. Verifique se a porta está livre:
   ```bash
   sudo netstat -tlnp | grep 8001
   ```

2. Verifique logs:
   ```bash
   sudo journalctl -u mcp-server -n 50
   ```

3. Verifique variáveis de ambiente:
   ```bash
   cat .env
   ```

### Erro de import no Python

Execute a partir do diretório correto:
```bash
cd /caminho/para/personal_agent
python3 -m mcp_server.main
```

---

## 📚 Documentação

- **Documentação completa:** `docs/MVP_AGENTE_PESSOAL.md`
- **Guia do fluxo n8n:** `workflows/N8N_WORKFLOW_GUIDE.md`
- **Guia de setup:** `SETUP.md`
- **Guia de configuração:** `CONFIGURAR.md`

---

## 💡 Dicas

1. **Senha segura:** Use uma senha forte para o banco de dados
2. **Backup:** Configure backups regulares do banco
3. **Logs:** Monitore os logs do servidor MCP regularmente
4. **Testes:** Teste cada etapa antes de prosseguir

---

**Pronto para começar! 🎉**
