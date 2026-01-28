# ✅ Servidor MCP está Rodando - Ajustar URL no n8n

## Status do Servidor
✅ **Servidor MCP está ATIVO e funcionando:**
- Rodando há 17 horas
- Porta 8001 escutando em `0.0.0.0:8001`
- Health check OK: `{"status":"healthy","database":"connected"}`

## Problema
O n8n não consegue conectar. Isso pode ser porque:

1. **n8n está em container/Docker** → precisa usar IP do host
2. **n8n está em outro servidor** → precisa usar hostname/IP público
3. **Firewall bloqueando** → precisa liberar porta 8001

## Soluções

### Opção 1: Se n8n está no MESMO servidor

**URL no n8n:**
```
http://localhost:8001/mcp/detect
```
ou
```
http://127.0.0.1:8001/mcp/detect
```

### Opção 2: Se n8n está em CONTAINER/Docker

**URL no n8n:**
```
http://host.docker.internal:8001/mcp/detect
```
ou use o IP do host:
```
http://[IP_DO_HOST]:8001/mcp/detect
```

### Opção 3: Se n8n está em OUTRO servidor

**URL no n8n:**
```
http://srv1140258.hstgr.cloud:8001/mcp/detect
```

**IMPORTANTE:** Verificar se o firewall permite conexões externas:
```bash
sudo ufw status | grep 8001
# Se não estiver liberado:
sudo ufw allow 8001/tcp
```

## JSON Corrigido para n8n

### Para n8n no mesmo servidor:
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

### Para n8n em container/Docker:
```json
{
  "parameters": {
    "method": "POST",
    "url": "http://host.docker.internal:8001/mcp/detect",
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

### Para n8n em outro servidor:
```json
{
  "parameters": {
    "method": "POST",
    "url": "http://srv1140258.hstgr.cloud:8001/mcp/detect",
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

## Testar Conexão do n8n

No n8n, você pode testar a conexão criando um node HTTP Request simples:

1. Adicione um node **HTTP Request**
2. Configure:
   - **Method:** GET
   - **URL:** `http://localhost:8001/health` (ou a URL apropriada)
3. Execute e veja se retorna: `{"status":"healthy","database":"connected"}`

Se funcionar, o problema é apenas a URL no node "MCP: Detectar Intenção".

## Verificar Firewall (se necessário)

```bash
# Verificar status do firewall
sudo ufw status

# Se a porta 8001 não estiver liberada:
sudo ufw allow 8001/tcp
sudo ufw reload
```
