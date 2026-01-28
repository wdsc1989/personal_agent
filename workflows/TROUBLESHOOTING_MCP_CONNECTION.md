# 🔧 Troubleshooting - Erro de Conexão MCP

## Erro
```
The service refused the connection - perhaps it is offline
```

## Verificações Necessárias

### 1. Verificar se o Servidor MCP está Rodando

**No servidor (SSH):**
```bash
# Verificar status do serviço
sudo systemctl status mcp-server

# Se não estiver rodando, iniciar:
sudo systemctl start mcp-server

# Verificar logs se houver erro:
sudo journalctl -u mcp-server -n 50 --no-pager
```

### 2. Verificar se a Porta 8001 está Escutando

```bash
# Verificar se a porta está aberta
sudo netstat -tlnp | grep 8001
# OU
sudo ss -tlnp | grep 8001

# Deve mostrar algo como:
# tcp  0  0  0.0.0.0:8001  0.0.0.0:*  LISTEN  PID/python
```

### 3. Testar Conexão Localmente

```bash
# No servidor, testar se o servidor responde:
curl http://localhost:8001/health

# Deve retornar:
# {"status":"ok"}
```

### 4. Verificar Firewall

```bash
# Verificar se a porta está liberada
sudo ufw status | grep 8001

# Se não estiver, liberar:
sudo ufw allow 8001/tcp
```

### 5. Ajustar URL no n8n

**Se o n8n está no mesmo servidor:**
- Use: `http://localhost:8001/mcp/detect`
- OU: `http://127.0.0.1:8001/mcp/detect`

**Se o n8n está em outro servidor/container:**
- Use o IP do servidor: `http://srv1140258.hstgr.cloud:8001/mcp/detect`
- OU o IP interno: `http://[IP_INTERNO]:8001/mcp/detect`

## Solução Rápida

### Passo 1: Iniciar Servidor MCP

```bash
# No servidor
cd /opt/personal_agent
sudo systemctl start mcp-server
sudo systemctl enable mcp-server
sudo systemctl status mcp-server
```

### Passo 2: Verificar se está Funcionando

```bash
curl http://localhost:8001/health
```

### Passo 3: Ajustar URL no n8n

**Node "MCP: Detectar Intenção":**
- **URL:** `http://localhost:8001/mcp/detect` (se n8n está no mesmo servidor)
- **OU:** `http://srv1140258.hstgr.cloud:8001/mcp/detect` (se n8n está em outro lugar)

## JSON Corrigido para n8n

```json
{
  "parameters": {
    "method": "POST",
    "url": "http://localhost:8001/mcp/detect",
    "sendBody": true,
    "bodyContentType": "json",
    "jsonBody": "={\n  \"text\": \"{{ $json.text }}\",\n  \"context\": {}\n}",
    "options": {}
  },
  "name": "MCP: Detectar Intenção",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2
}
```

## Comandos Úteis

```bash
# Reiniciar servidor MCP
sudo systemctl restart mcp-server

# Ver logs em tempo real
sudo journalctl -u mcp-server -f

# Verificar processos Python rodando
ps aux | grep uvicorn

# Matar processo se necessário
sudo pkill -f "uvicorn main:app"
```

## Se o Problema Persistir

1. **Verificar se o venv está correto:**
   ```bash
   ls -la /opt/personal_agent/venv/bin/python3
   ```

2. **Verificar se as dependências estão instaladas:**
   ```bash
   /opt/personal_agent/venv/bin/pip list | grep fastapi
   ```

3. **Testar manualmente:**
   ```bash
   cd /opt/personal_agent/mcp_server
   /opt/personal_agent/venv/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8001
   ```
