# 🔄 Atualizar Servidor - Personal Agent

## Comandos para Atualizar no Servidor

Após fazer push das alterações, execute estes comandos no servidor:

### 1. Conectar ao Servidor

```bash
ssh root@srv1140258.hstgr.cloud
```

### 2. Atualizar Código do Repositório

```bash
cd /opt/personal_agent
git pull origin master
```

### 3. Atualizar Arquivo .env (se necessário)

Se você alterou a senha no `.env` localmente, atualize também no servidor:

```bash
cd /opt/personal_agent
nano .env
```

**IMPORTANTE:** 
- Use `localhost` como host (não o hostname externo)
- Se a senha contiver caracteres especiais como `@`, codifique-os:
  - `@` → `%40`
  - `#` → `%23`
  - `$` → `%24`
  - etc.

Exemplo:
```env
DATABASE_URL_PERSONAL=postgresql://personal_agent_user:senha_sem_especiais@localhost:5432/personal_agent_db
```

### 4. Testar Conexão

```bash
cd /opt/personal_agent
source venv/bin/activate
python3 scripts/test_connection.py
```

### 5. Reiniciar Servidor MCP (se necessário)

Se houver mudanças no código do servidor MCP:

```bash
sudo systemctl restart mcp-server
sudo systemctl status mcp-server
```

### 6. Verificar Logs

```bash
sudo journalctl -u mcp-server -f
```

---

## Atualização Rápida (Tudo de Uma Vez)

```bash
ssh root@srv1140258.hstgr.cloud
cd /opt/personal_agent
git pull origin master
source venv/bin/activate
python3 scripts/test_connection.py
sudo systemctl restart mcp-server
sudo systemctl status mcp-server
```

---

## Se Houver Problemas

### Erro de conexão com banco:

1. Verificar se PostgreSQL está rodando:
   ```bash
   sudo systemctl status postgresql
   ```

2. Verificar arquivo .env:
   ```bash
   cat /opt/personal_agent/.env
   ```

3. Testar conexão manual:
   ```bash
   psql -U personal_agent_user -d personal_agent_db -h localhost
   ```

### Servidor MCP não inicia:

1. Ver logs:
   ```bash
   sudo journalctl -u mcp-server -n 50
   ```

2. Testar manualmente:
   ```bash
   cd /opt/personal_agent
   source venv/bin/activate
   cd mcp_server
   python3 main.py
   ```

---

**Atualização concluída! ✅**
