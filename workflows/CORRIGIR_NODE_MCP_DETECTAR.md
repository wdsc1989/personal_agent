# 🔧 Corrigir Node "MCP: Detectar Intenção" - Não Sai do Node

## Problema
O node conecta com sucesso (`http://172.17.0.1:8001/mcp/detect`) mas:
- Executa sem ação
- Não sai do node (fica travado)

## Causas Possíveis

1. **Node não recebe dados de entrada** → `$json.text` está vazio/undefined
2. **Body não está sendo enviado corretamente** → Formato JSON incorreto
3. **Timeout ou espera infinita** → Servidor não retorna resposta
4. **Resposta não está sendo processada** → Formato de resposta incorreto

## Solução

### 1. Verificar Dados de Entrada

O node precisa receber dados do node anterior. Verifique se há um node antes de "MCP: Detectar Intenção" que passa `text`.

**Exemplo de node anterior (Set):**
```json
{
  "parameters": {
    "fields": {
      "values": [
        {
          "name": "text",
          "stringValue": "={{ $json.message.text || $json.text || '' }}"
        }
      ]
    }
  },
  "name": "Preparar Texto",
  "type": "n8n-nodes-base.set"
}
```

### 2. Node "MCP: Detectar Intenção" Corrigido

```json
{
  "parameters": {
    "method": "POST",
    "url": "http://172.17.0.1:8001/mcp/detect",
    "sendBody": true,
    "bodyContentType": "json",
    "jsonBody": "={\n  \"text\": \"{{ $json.text || $json.message?.text || '' }}\",\n  \"context\": {}\n}",
    "options": {
      "timeout": 10000,
      "response": {
        "response": {
          "responseFormat": "json"
        }
      }
    }
  },
  "name": "MCP: Detectar Intenção",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2
}
```

### 3. Adicionar Node de Debug (Opcional)

Para verificar o que está sendo enviado, adicione um node Code antes:

```json
{
  "parameters": {
    "jsCode": "const input = $input.first().json;\nreturn {\n  text: input.text || input.message?.text || 'SEM TEXTO',\n  debug: JSON.stringify(input, null, 2)\n};"
  },
  "name": "Debug: Ver Dados",
  "type": "n8n-nodes-base.code",
  "typeVersion": 2
}
```

### 4. Verificar Resposta do Servidor

O servidor deve retornar:
```json
{
  "action": "INSERT",
  "entity": "contas_pagar",
  "confidence": 0.9,
  "extracted_info": {}
}
```

## Configuração Completa do Node

**No n8n, configure o node assim:**

1. **Method:** POST
2. **URL:** `http://172.17.0.1:8001/mcp/detect`
3. **Send Body:** ✅ Sim
4. **Body Content Type:** JSON
5. **JSON Body:**
   ```json
   {
     "text": "{{ $json.text || $json.message?.text || '' }}",
     "context": {}
   }
   ```
6. **Options:**
   - **Timeout:** 10000 (10 segundos)
   - **Response Format:** JSON

## Teste Manual

Teste diretamente no servidor:

```bash
curl -X POST http://localhost:8001/mcp/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "Adicionar conta: Fornecedor XYZ, vencimento 15/01/2025, R$ 1.500", "context": {}}'
```

**Resposta esperada:**
```json
{
  "action": "INSERT",
  "entity": "contas_pagar",
  "confidence": 0.9,
  "extracted_info": {}
}
```

## Checklist

- [ ] Node anterior está passando `text` corretamente
- [ ] URL está correta: `http://172.17.0.1:8001/mcp/detect`
- [ ] Body Content Type está como "JSON"
- [ ] JSON Body tem `text` e `context`
- [ ] Timeout configurado (10 segundos)
- [ ] Response Format está como "JSON"

## Se Ainda Não Funcionar

1. **Verifique logs do servidor MCP:**
   ```bash
   sudo journalctl -u mcp-server -n 50 --no-pager
   ```

2. **Teste com dados hardcoded:**
   ```json
   {
     "text": "Adicionar conta: Teste, vencimento 15/01/2025, R$ 100",
     "context": {}
   }
   ```

3. **Verifique se o node está conectado ao próximo:**
   - O node precisa ter uma conexão de saída
   - Verifique se há um node após "MCP: Detectar Intenção"
