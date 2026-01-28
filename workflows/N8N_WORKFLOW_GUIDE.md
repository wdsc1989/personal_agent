# Guia do Fluxo n8n - Agente Pessoal MVP

Este documento descreve como configurar o fluxo n8n completo para o Agente Pessoal com integração MCP e sistema de confirmação.

## Pré-requisitos

1. Servidor MCP rodando em `http://localhost:8001`
2. Banco de dados `personal_agent_db` criado e configurado
3. Credenciais do Telegram Bot configuradas no n8n
4. Credenciais do PostgreSQL configuradas no n8n

## Estrutura do Fluxo

### 1. Telegram Trigger - Escutar Mensagens

**Node:** `Telegram Trigger`

**Configuração:**
- **Credential:** Telegram Bot
- **Updates:** `message`
- **Additional Fields:**
  - `chat_id` → `{{ $json.message.chat.id }}`
  - `message_id` → `{{ $json.message.message_id }}`
  - `text` → `{{ $json.message.text }}`
  - `voice` → `{{ $json.message.voice }}`
  - `from_user` → `{{ $json.message.from }}`

### 2. Detectar Tipo de Entrada

**Node:** `IF` - `É Áudio?`

**Condição:**
```javascript
{{ $json.voice !== undefined && $json.voice !== null }}
```

**Outputs:**
- `true` → Vai para "Obter Arquivo de Voz"
- `false` → Vai para "Preparar Dados"

### 3. Transcrever Áudio (se for áudio)

**Node:** `Telegram` - `Obter Arquivo de Voz`

**Configuração:**
- **Operation:** `Get File`
- **File ID:** `{{ $json.voice.file_id }}`

**Node:** `OpenAI` - `Voz para Texto`

**Configuração:**
- **Resource:** `Audio`
- **Operation:** `Transcribe`
- **File:** `{{ $json.data }}`
- **Language:** `pt`

**Node:** `Set` - `Mesclar Texto`

**Configuração:**
- **Keep Only Set Fields:** `false`
- **Fields to Set:**
  - `text` → `{{ $json.text }}`
  - `transcription` → `{{ $('Voz para Texto').item.json.text }}`
  - `final_text` → `{{ $json.transcription || $json.text }}`

### 4. Preparar Dados

**Node:** `Set` - `Preparar Dados`

**Configuração:**
- **Fields to Set:**
  - `text` → `{{ $json.final_text || $json.text }}`
  - `chat_id` → `{{ $json.chat_id }}`
  - `message_id` → `{{ $json.message_id }}`
  - `telegram_user` → `{{ $json.from_user }}`
  - `context` → `{{ { "previous_action": null } }}`

### 5. MCP: Detectar Intenção

**Node:** `HTTP Request` - `MCP: Detectar Intenção`

**Configuração:**
- **Method:** `POST`
- **URL:** `http://localhost:8001/mcp/detect`
- **Authentication:** `None`
- **Body Content Type:** `JSON`
- **Body:**
```json
{
  "text": "{{ $json.text }}",
  "context": {{ $json.context }}
}
```

**Output:**
- `action` → Ação detectada (INSERT, UPDATE, DELETE, LIST, REPORT, OTHER)
- `entity` → Entidade (`contas_pagar`)
- `confidence` → Confiança (0-1)

### 6. Roteador de Ação

**Node:** `Switch` - `Roteador de Ação`

**Configuração:**
- **Mode:** `Rules`
- **Rules:**
  - `INSERT` → `{{ $json.action === 'INSERT' }}`
  - `UPDATE` → `{{ $json.action === 'UPDATE' }}`
  - `DELETE` → `{{ $json.action === 'DELETE' }}`
  - `LIST` → `{{ $json.action === 'LIST' }}`
  - `REPORT` → `{{ $json.action === 'REPORT' }}`
  - `OTHER` → `{{ true }}` (fallback)

### 7. Processamento INSERT/UPDATE/DELETE

#### 7.1 MCP: Extrair Dados

**Node:** `HTTP Request` - `MCP: Extrair Dados`

**Configuração:**
- **Method:** `POST`
- **URL:** `http://localhost:8001/mcp/extract`
- **Body:**
```json
{
  "text": "{{ $('Preparar Dados').item.json.text }}",
  "action": "{{ $json.action }}",
  "context": {{ $('Preparar Dados').item.json.context }}
}
```

#### 7.2 MCP: Validar Dados

**Node:** `HTTP Request` - `MCP: Validar Dados`

**Configuração:**
- **Method:** `POST`
- **URL:** `http://localhost:8001/mcp/validate`
- **Body:**
```json
{
  "data": {{ $json.data }},
  "action": "{{ $('MCP: Detectar Intenção').item.json.action }}"
}
```

#### 7.3 Verificar Validação

**Node:** `IF` - `Verificar Validação`

**Condição:**
```javascript
{{ $json.valid === true }}
```

**Outputs:**
- `true` → Vai para "MCP: Formatar Confirmação"
- `false` → Vai para "Enviar Erro de Validação"

**Node:** `Telegram` - `Enviar Erro de Validação`

**Configuração:**
- **Operation:** `Send Message`
- **Chat ID:** `{{ $('Preparar Dados').item.json.chat_id }}`
- **Text:**
```
❌ **Erro de Validação**

{{ $json.errors.join('\n') }}

Por favor, corrija os dados e tente novamente.
```

#### 7.4 MCP: Formatar Confirmação

**Node:** `HTTP Request` - `MCP: Formatar Confirmação`

**Configuração:**
- **Method:** `POST`
- **URL:** `http://localhost:8001/mcp/format-confirmation`
- **Body:**
```json
{
  "action": "{{ $('MCP: Detectar Intenção').item.json.action }}",
  "data": {{ $('MCP: Extrair Dados').item.json.data }},
  "old_data": null
}
```

#### 7.5 Enviar Confirmação

**Node:** `Telegram` - `Enviar Confirmação`

**Configuração:**
- **Operation:** `Send Message`
- **Chat ID:** `{{ $('Preparar Dados').item.json.chat_id }}`
- **Parse Mode:** `Markdown`
- **Text:** `{{ $json.message }}`

#### 7.6 Aguardar Confirmação

**Node:** `Wait` - `Aguardar Confirmação`

**Configuração:**
- **Resume:** `When Last Node Finishes`
- **Wait Time:** `60` segundos

**Node:** `Telegram Trigger` - `Aguardar Resposta`

**Configuração:**
- **Credential:** Mesmo Telegram Bot
- **Updates:** `message`
- **Filter:** `{{ $json.message.chat.id === $('Preparar Dados').item.json.chat_id }}`

#### 7.7 Verificar Confirmação

**Node:** `Code` - `Verificar Confirmação`

**Código:**
```javascript
const resposta = $input.item.json.text.toLowerCase().trim();
const confirmacoes = ['sim', 's', 'confirmar', 'ok', 'yes', 'y'];
const cancelamentos = ['não', 'nao', 'n', 'cancelar', 'cancel', 'no'];

if (confirmacoes.includes(resposta)) {
  return { confirmed: true };
} else if (cancelamentos.includes(resposta)) {
  return { confirmed: false };
} else {
  return { confirmed: false, invalid: true };
}
```

#### 7.8 Executar ou Cancelar

**Node:** `Switch` - `Executar ou Cancelar`

**Configuração:**
- **Mode:** `Rules`
- **Rules:**
  - `Confirmado` → `{{ $json.confirmed === true }}`
  - `Cancelado` → `{{ $json.confirmed === false }}`

**Node:** `Telegram` - `Enviar Cancelamento`

**Configuração:**
- **Operation:** `Send Message`
- **Chat ID:** `{{ $('Preparar Dados').item.json.chat_id }}`
- **Text:** `❌ Operação cancelada.`

#### 7.9 Executar Operação

**Node:** `PostgreSQL` - `Executar Inserção` (para INSERT)

**Configuração:**
- **Operation:** `Execute Query`
- **Query:**
```sql
INSERT INTO contas_pagar (
  usuario_telegram_id, nome_credor, descricao, valor_total,
  data_vencimento, categoria, status
) VALUES (
  (SELECT id FROM usuarios_telegram WHERE telegram_id = $1),
  $2, $3, $4, $5, $6, 'pendente'
)
RETURNING id, nome_credor, valor_total, data_vencimento;
```
- **Parameters:**
  - `{{ $('Preparar Dados').item.json.telegram_user.id }}`
  - `{{ $('MCP: Extrair Dados').item.json.data.nome_credor }}`
  - `{{ $('MCP: Extrair Dados').item.json.data.descricao || null }}`
  - `{{ $('MCP: Extrair Dados').item.json.data.valor_total }}`
  - `{{ $('MCP: Extrair Dados').item.json.data.data_vencimento }}`
  - `{{ $('MCP: Extrair Dados').item.json.data.categoria || null }}`

**Node:** `PostgreSQL` - `Executar Atualização` (para UPDATE)

**Configuração:**
- **Operation:** `Execute Query`
- **Query:**
```sql
UPDATE contas_pagar
SET nome_credor = $1, valor_total = $2, data_vencimento = $3,
    categoria = $4, atualizado_em = CURRENT_TIMESTAMP
WHERE id = $5 AND usuario_telegram_id = (
  SELECT id FROM usuarios_telegram WHERE telegram_id = $6
)
RETURNING id, nome_credor, valor_total;
```

**Node:** `PostgreSQL` - `Executar Exclusão` (para DELETE)

**Configuração:**
- **Operation:** `Execute Query`
- **Query:**
```sql
DELETE FROM contas_pagar
WHERE id = $1 AND usuario_telegram_id = (
  SELECT id FROM usuarios_telegram WHERE telegram_id = $2
)
RETURNING id, nome_credor;
```

#### 7.10 Enviar Resultado

**Node:** `Telegram` - `Enviar Sucesso`

**Configuração:**
- **Operation:** `Send Message`
- **Chat ID:** `{{ $('Preparar Dados').item.json.chat_id }}`
- **Parse Mode:** `Markdown`
- **Text:**
```
✅ **Conta registrada com sucesso!**

**ID:** {{ $json.id }}
**Credor:** {{ $json.nome_credor }}
**Valor:** R$ {{ $json.valor_total }}
**Vencimento:** {{ $json.data_vencimento }}
```

### 8. Processamento LIST

#### 8.1 MCP: Extrair Filtros

**Node:** `HTTP Request` - `MCP: Extrair Filtros`

**Configuração:**
- **Method:** `POST`
- **URL:** `http://localhost:8001/mcp/extract`
- **Body:**
```json
{
  "text": "{{ $('Preparar Dados').item.json.text }}",
  "action": "LIST",
  "context": {{ $('Preparar Dados').item.json.context }}
}
```

#### 8.2 MCP: Listar Contas

**Node:** `HTTP Request` - `MCP: Listar Contas`

**Configuração:**
- **Method:** `POST`
- **URL:** `http://localhost:8001/mcp/list`
- **Body:**
```json
{
  "usuario_telegram_id": {{ $('Preparar Dados').item.json.telegram_user.id }},
  "data_inicial": "{{ $json.data.data_inicial || null }}",
  "data_final": "{{ $json.data.data_final || null }}",
  "status": "{{ $json.data.status || null }}",
  "categoria": "{{ $json.data.categoria || null }}"
}
```

#### 8.3 Enviar Lista

**Node:** `Code` - `Formatar Lista`

**Código:**
```javascript
const contas = $input.item.json.contas;
let mensagem = `📋 **Suas Contas**\n\n`;
mensagem += `Total: ${contas.length} conta(s)\n`;
mensagem += `Valor Total: R$ ${$input.item.json.total_valor.toFixed(2)}\n\n`;

contas.forEach((conta, index) => {
  mensagem += `${index + 1}. **${conta.nome_credor}**\n`;
  mensagem += `   Valor: R$ ${conta.valor_total.toFixed(2)}\n`;
  mensagem += `   Vencimento: ${conta.data_vencimento}\n`;
  mensagem += `   Status: ${conta.status}\n\n`;
});

return { message: mensagem };
```

**Node:** `Telegram` - `Enviar Lista`

**Configuração:**
- **Operation:** `Send Message`
- **Chat ID:** `{{ $('Preparar Dados').item.json.chat_id }}`
- **Parse Mode:** `Markdown`
- **Text:** `{{ $json.message }}`

### 9. Tratamento de Erros

**Node:** `Code` - `Tratar Erro`

**Configuração:**
- **On Error:** Conectado a todos os nodes críticos

**Código:**
```javascript
const error = $input.error;
return {
  error: true,
  message: `❌ Erro: ${error.message}`,
  chat_id: $('Preparar Dados').item.json.chat_id
};
```

**Node:** `Telegram` - `Enviar Erro`

**Configuração:**
- **Operation:** `Send Message`
- **Chat ID:** `{{ $json.chat_id }}`
- **Text:** `{{ $json.message }}`

## Variáveis de Ambiente Necessárias

No n8n, configure as seguintes variáveis:

- `MCP_SERVER_URL`: `http://localhost:8001`
- `DATABASE_URL_PERSONAL`: `postgresql://personal_agent_user:senha@localhost:5432/personal_agent_db`

## Notas Importantes

1. **Memória de Contexto:** Use o node `Memory Buffer` para manter histórico de conversas
2. **Timeout:** O timeout de confirmação é de 60 segundos
3. **Validação:** Todos os dados são validados antes de qualquer operação
4. **Confirmação:** Todas as operações CRUD requerem confirmação explícita

## Exemplos de Comandos

- **Inserir:** "Adicionar conta: Fornecedor XYZ, vencimento 15/01/2025, R$ 1.500"
- **Listar:** "Mostrar minhas contas"
- **Listar por período:** "Contas de janeiro de 2025"
- **Atualizar:** "Atualizar conta ID 5: valor R$ 2.000"
- **Deletar:** "Excluir conta ID 5"
