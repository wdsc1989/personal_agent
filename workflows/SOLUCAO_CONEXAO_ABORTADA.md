# 🔧 Solução: Conexão Abortada no Node MCP

## Erro
```
The connection was aborted, perhaps the server is offline
```

## Possíveis Causas

1. **Servidor está caindo durante o processamento**
2. **Timeout muito curto** → Servidor demora para processar
3. **Problema com banco de dados** → Conexão sendo fechada durante a query
4. **Sessão do banco não sendo fechada** → Acumula conexões e fecha

## Soluções

### 1. Verificar Logs do Servidor MCP

```bash
# Ver logs em tempo real
sudo journalctl -u mcp-server -f

# Ver últimas 100 linhas
sudo journalctl -u mcp-server -n 100 --no-pager
```

**Procure por:**
- Erros de banco de dados
- Timeouts
- Conexões sendo fechadas
- Erros de memória

### 2. Testar Endpoint Manualmente

```bash
# Teste simples
curl -X POST http://localhost:8001/mcp/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "Adicionar conta: Teste, R$ 100", "context": {}}' \
  -v

# Se funcionar, o problema é no n8n
# Se não funcionar, o problema é no servidor
```

### 3. Node n8n com Retry e Timeout Maior

**JSON corrigido:**
```json
{
  "parameters": {
    "method": "POST",
    "url": "http://172.17.0.1:8001/mcp/detect",
    "sendBody": true,
    "bodyContentType": "json",
    "jsonBody": "={\n  \"text\": \"{{ $json.text || $json.message?.text || '' }}\",\n  \"context\": {}\n}",
    "options": {
      "timeout": 30000,
      "retry": {
        "maxRetries": 3,
        "retryOnFail": true
      },
      "response": {
        "response": {
          "responseFormat": "json",
          "fullResponse": false
        }
      }
    }
  },
  "name": "MCP: Detectar Intenção",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "onError": "continueErrorOutput"
}
```

**Mudanças:**
- ✅ Timeout aumentado: 30 segundos (30000ms)
- ✅ Retry automático: 3 tentativas
- ✅ Continue on Error: Não para o fluxo se falhar

### 4. Verificar Conexões do Banco de Dados

```bash
# No servidor, verificar conexões ativas
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity WHERE datname='personal_agent_db';"

# Ver conexões por usuário
sudo -u postgres psql -c "SELECT usename, count(*) FROM pg_stat_activity WHERE datname='personal_agent_db' GROUP BY usename;"
```

### 5. Verificar Recursos do Servidor

```bash
# Ver uso de memória e CPU
top -p $(pgrep -f "uvicorn main:app")

# Ver uso de memória do serviço
systemctl status mcp-server | grep Memory
```

### 6. Ajustar Timeout do Uvicorn (se necessário)

Editar arquivo de serviço:
```bash
sudo nano /etc/systemd/system/mcp-server.service
```

Adicionar timeout:
```ini
[Service]
...
ExecStart=/opt/personal_agent/venv/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8001 --timeout-keep-alive 30
TimeoutStopSec=60
```

Recarregar:
```bash
sudo systemctl daemon-reload
sudo systemctl restart mcp-server
```

## Teste Passo a Passo

1. **Teste health check:**
   ```bash
   curl http://localhost:8001/health
   ```

2. **Teste endpoint detect:**
   ```bash
   curl -X POST http://localhost:8001/mcp/detect \
     -H "Content-Type: application/json" \
     -d '{"text": "teste", "context": {}}'
   ```

3. **Se funcionar, teste do n8n:**
   - Use o JSON corrigido acima
   - Execute o workflow
   - Verifique logs do servidor durante a execução

## Se o Problema Persistir

### Opção 1: Adicionar Node de Retry Manual

Crie um sub-workflow que tenta 3 vezes:

```json
{
  "nodes": [
    {
      "name": "Tentar 1",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "http://172.17.0.1:8001/mcp/detect",
        ...
      },
      "onError": "continueErrorOutput"
    },
    {
      "name": "Se Erro, Tentar 2",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "conditions": [{
            "leftValue": "={{ $json.error }}",
            "operator": { "type": "boolean", "operation": "true" }
          }]
        }
      }
    }
  ]
}
```

### Opção 2: Verificar Problema no Código do Servidor

O problema pode estar no `mcp_detector.py` ou na sessão do banco. Verifique se:
- A sessão está sendo fechada corretamente
- Não há queries muito lentas
- Não há deadlocks

## Checklist de Diagnóstico

- [ ] Health check funciona: `curl http://localhost:8001/health`
- [ ] Endpoint detect funciona manualmente
- [ ] Logs do servidor não mostram erros
- [ ] Conexões do banco não estão acumulando
- [ ] Memória e CPU estão OK
- [ ] Timeout aumentado no n8n (30s)
- [ ] Retry configurado (3 tentativas)
- [ ] Continue on Error ativado

---

**Arquivo JSON corrigido:** `workflows/NODE_MCP_DETECTAR_INTENCAO_ROBUSTO.json`
