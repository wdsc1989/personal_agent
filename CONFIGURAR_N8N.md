# 📱 Configurar Fluxo n8n - Agente Pessoal

## Status Atual

✅ Servidor MCP rodando em `http://localhost:8001`
✅ Banco de dados configurado e funcionando
✅ Health check OK

---

## 📋 Passo 1: Acessar n8n

1. Acesse o n8n no servidor (geralmente `http://srv1140258.hstgr.cloud:5678` ou porta configurada)
2. Faça login

---

## 📋 Passo 2: Criar Novo Fluxo

1. Clique em **"Workflows"** → **"New Workflow"**
2. Nomeie: **"Agente Pessoal - Contas a Pagar"**

---

## 📋 Passo 3: Configurar Telegram Trigger

### 3.1 Adicionar Node

1. Arraste um node **"Telegram Trigger"** para o canvas
2. Nome: **"Escutar Mensagens"**

### 3.2 Configurar Credenciais

1. Clique em **"Create New Credential"** ou selecione existente
2. Configure:
   - **Bot Token:** Token do seu bot Telegram
   - Salve as credenciais

### 3.3 Configurar Node

- **Updates:** `message`
- **Additional Fields:**
  - Deixe padrão (captura automaticamente chat_id, message_id, text, voice, etc.)

---

## 📋 Passo 4: Detectar Tipo de Entrada (Texto ou Áudio)

### 4.1 Adicionar Node Set

1. Adicione node **"Set"**
2. Nome: **"Preparar Dados"**
3. Configure:
   - **Keep Only Set Fields:** `false`
   - **Fields to Set:**
     - `chat_id` → `{{ $json.message.chat.id }}`
     - `message_id` → `{{ $json.message.message_id }}`
     - `text` → `{{ $json.message.text || "" }}`
     - `voice` → `{{ $json.message.voice || null }}`
     - `from_user` → `{{ $json.message.from }}`

### 4.2 Adicionar Node IF

1. Adicione node **"IF"**
2. Nome: **"É Áudio?"**
3. Condição:
   ```javascript
   {{ $json.voice !== undefined && $json.voice !== null }}
   ```

### 4.3 Configurar Transcrição de Áudio (se for áudio)

**No caminho TRUE do IF:**

1. Adicione node **"Telegram"** → **"Get File"**
   - Nome: **"Obter Arquivo de Voz"**
   - **File ID:** `{{ $json.voice.file_id }}`

2. Adicione node **"OpenAI"** → **"Transcribe"**
   - Nome: **"Voz para Texto"**
   - **File:** `{{ $json.data }}`
   - **Language:** `pt`

3. Adicione node **"Set"**
   - Nome: **"Mesclar Texto"**
   - **Fields to Set:**
     - `text` → `{{ $('Voz para Texto').item.json.text }}`
     - `chat_id` → `{{ $('Preparar Dados').item.json.chat_id }}`
     - `from_user` → `{{ $('Preparar Dados').item.json.from_user }}`

**No caminho FALSE do IF:**

1. Conecte diretamente ao próximo passo (já tem texto)

---

## 📋 Passo 5: Integração com Servidor MCP

### 5.1 MCP: Detectar Intenção

1. Adicione node **"HTTP Request"**
2. Nome: **"MCP: Detectar Intenção"**
3. Configure:
   - **Method:** `POST`
   - **URL:** `http://localhost:8001/mcp/detect`
   - **Authentication:** `None`
   - **Body Content Type:** `JSON`
   - **Body:**
   ```json
   {
     "text": "{{ $json.text || $('Preparar Dados').item.json.text }}",
     "context": {}
   }
   ```

### 5.2 Roteador de Ação

1. Adicione node **"Switch"**
2. Nome: **"Roteador de Ação"**
3. **Mode:** `Rules`
4. **Rules:**
   - `INSERT` → `{{ $json.action === 'INSERT' }}`
   - `UPDATE` → `{{ $json.action === 'UPDATE' }}`
   - `DELETE` → `{{ $json.action === 'DELETE' }}`
   - `LIST` → `{{ $json.action === 'LIST' }}`
   - `REPORT` → `{{ $json.action === 'REPORT' }}`
   - `OTHER` → `{{ true }}` (fallback)

---

## 📋 Passo 6: Processar INSERT/UPDATE/DELETE (com Confirmação)

### 6.1 MCP: Extrair Dados

1. Adicione node **"HTTP Request"**
2. Nome: **"MCP: Extrair Dados"**
3. Configure:
   - **Method:** `POST`
   - **URL:** `http://localhost:8001/mcp/extract`
   - **Body:**
   ```json
   {
     "text": "{{ $('Preparar Dados').item.json.text }}",
     "action": "{{ $('MCP: Detectar Intenção').item.json.action }}",
     "context": {}
   }
   ```

### 6.2 MCP: Validar Dados

1. Adicione node **"HTTP Request"**
2. Nome: **"MCP: Validar Dados"**
3. Configure:
   - **Method:** `POST`
   - **URL:** `http://localhost:8001/mcp/validate`
   - **Body:**
   ```json
   {
     "data": {{ $json.data }},
     "action": "{{ $('MCP: Detectar Intenção').item.json.action }}"
   }
   ```

### 6.3 Verificar Validação

1. Adicione node **"IF"**
2. Nome: **"Verificar Validação"**
3. Condição:
   ```javascript
   {{ $json.valid === true }}
   ```

**Se FALSE (erro):**
- Adicione node **"Telegram"** → **"Send Message"**
- Nome: **"Enviar Erro de Validação"**
- **Chat ID:** `{{ $('Preparar Dados').item.json.chat_id }}`
- **Text:**
  ```
  ❌ **Erro de Validação**
  
  {{ $json.errors.join('\n') }}
  
  Por favor, corrija os dados e tente novamente.
  ```

### 6.4 MCP: Formatar Confirmação

1. Adicione node **"HTTP Request"**
2. Nome: **"MCP: Formatar Confirmação"**
3. Configure:
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

### 6.5 Enviar Confirmação

1. Adicione node **"Telegram"** → **"Send Message"**
2. Nome: **"Enviar Confirmação"**
3. Configure:
   - **Chat ID:** `{{ $('Preparar Dados').item.json.chat_id }}`
   - **Parse Mode:** `Markdown`
   - **Text:** `{{ $json.message }}`

### 6.6 Aguardar Confirmação

1. Adicione node **"Wait"**
2. Nome: **"Aguardar Confirmação"**
3. Configure:
   - **Resume:** `When Last Node Finishes`
   - **Wait Time:** `60` segundos

4. Adicione node **"Telegram Trigger"**
5. Nome: **"Aguardar Resposta"**
6. Configure:
   - **Updates:** `message`
   - **Filter:** `{{ $json.message.chat.id === $('Preparar Dados').item.json.chat_id }}`

### 6.7 Verificar Confirmação

1. Adicione node **"Code"**
2. Nome: **"Verificar Confirmação"**
3. Código:
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

### 6.8 Executar ou Cancelar

1. Adicione node **"Switch"**
2. Nome: **"Executar ou Cancelar"**
3. **Mode:** `Rules`
4. **Rules:**
   - `Confirmado` → `{{ $json.confirmed === true }}`
   - `Cancelado` → `{{ $json.confirmed === false }}`

**Se Cancelado:**
- Adicione node **"Telegram"** → **"Send Message"**
- Nome: **"Enviar Cancelamento"**
- **Text:** `❌ Operação cancelada.`

**Se Confirmado:**
- Continue para executar operação

### 6.9 Executar Operação no Banco

**Para INSERT:**

1. Adicione node **"PostgreSQL"**
2. Nome: **"Executar Inserção"**
3. Configure:
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
     - `{{ $('Preparar Dados').item.json.from_user.id }}`
     - `{{ $('MCP: Extrair Dados').item.json.data.nome_credor }}`
     - `{{ $('MCP: Extrair Dados').item.json.data.descricao || null }}`
     - `{{ $('MCP: Extrair Dados').item.json.data.valor_total }}`
     - `{{ $('MCP: Extrair Dados').item.json.data.data_vencimento }}`
     - `{{ $('MCP: Extrair Dados').item.json.data.categoria || null }}`

**Para UPDATE e DELETE:** Configure queries similares conforme necessário.

### 6.10 Enviar Resultado

1. Adicione node **"Telegram"** → **"Send Message"**
2. Nome: **"Enviar Sucesso"**
3. Configure:
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

---

## 📋 Passo 7: Processar LIST (Listar Contas)

### 7.1 MCP: Extrair Filtros

1. Adicione node **"HTTP Request"**
2. Nome: **"MCP: Extrair Filtros"**
3. Configure:
   - **Method:** `POST`
   - **URL:** `http://localhost:8001/mcp/extract`
   - **Body:**
   ```json
   {
     "text": "{{ $('Preparar Dados').item.json.text }}",
     "action": "LIST",
     "context": {}
   }
   ```

### 7.2 MCP: Listar Contas

1. Adicione node **"HTTP Request"**
2. Nome: **"MCP: Listar Contas"**
3. Configure:
   - **Method:** `POST`
   - **URL:** `http://localhost:8001/mcp/list`
   - **Body:**
   ```json
   {
     "usuario_telegram_id": {{ $('Preparar Dados').item.json.from_user.id }},
     "data_inicial": "{{ $json.data.data_inicial || null }}",
     "data_final": "{{ $json.data.data_final || null }}",
     "status": "{{ $json.data.status || null }}",
     "categoria": "{{ $json.data.categoria || null }}"
   }
   ```

### 7.3 Format e Enviar Lista

1. Adicione node **"Code"**
2. Nome: **"Formatar Lista"**
3. Código:
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

4. Adicione node **"Telegram"** → **"Send Message"**
5. Nome: **"Enviar Lista"**
6. Configure:
   - **Chat ID:** `{{ $('Preparar Dados').item.json.chat_id }}`
   - **Parse Mode:** `Markdown`
   - **Text:** `{{ $json.message }}`

---

## 📋 Passo 8: Tratamento de Erros

1. Adicione node **"Code"**
2. Nome: **"Tratar Erro"**
3. Configure **"On Error"** em todos os nodes críticos apontando para este node
4. Código:
   ```javascript
   const error = $input.error;
   return {
     error: true,
     message: `❌ Erro: ${error.message}`,
     chat_id: $('Preparar Dados').item.json.chat_id
   };
   ```

5. Adicione node **"Telegram"** → **"Send Message"**
6. Nome: **"Enviar Erro"**
7. Configure:
   - **Chat ID:** `{{ $json.chat_id }}`
   - **Text:** `{{ $json.message }}`

---

## 📋 Passo 9: Criar/Atualizar Usuário Telegram

Antes de inserir contas, certifique-se de que o usuário existe:

1. Adicione node **"PostgreSQL"**
2. Nome: **"Criar ou Buscar Usuário"**
3. Configure:
   - **Operation:** `Execute Query`
   - **Query:**
   ```sql
   INSERT INTO usuarios_telegram (
     telegram_id, nome_usuario, primeiro_nome, ultimo_nome, codigo_idioma
   ) VALUES ($1, $2, $3, $4, 'pt-BR')
   ON CONFLICT (telegram_id) DO UPDATE SET
     ultimo_acesso = CURRENT_TIMESTAMP
   RETURNING id;
   ```
   - **Parameters:**
     - `{{ $json.from_user.id }}`
     - `{{ $json.from_user.username || null }}`
     - `{{ $json.from_user.first_name }}`
     - `{{ $json.from_user.last_name || null }}`

Execute este node logo após "Preparar Dados" e antes de processar ações.

---

## 📋 Passo 10: Ativar Fluxo

1. Clique no toggle **"Active"** no canto superior direito
2. O fluxo estará ativo e escutando mensagens do Telegram

---

## 🧪 Testar Fluxo

### Teste 1: Inserir Conta (Texto)

Envie via Telegram:
```
Adicionar conta: Fornecedor XYZ, vencimento 15/01/2025, R$ 1.500
```

### Teste 2: Listar Contas

Envie via Telegram:
```
Mostrar minhas contas
```

### Teste 3: Inserir Conta (Voz)

Envie um áudio via Telegram com o mesmo conteúdo.

---

## 📝 Variáveis de Ambiente no n8n

Configure no n8n (Settings → Environment Variables):

- `MCP_SERVER_URL`: `http://localhost:8001`
- `DATABASE_URL_PERSONAL`: `postgresql://personal_agent_user:Wc153624@localhost:5432/personal_agent_db`

---

## 🔗 Conexões do Fluxo

```
Escutar Mensagens
  ↓
Preparar Dados
  ↓
É Áudio? (IF)
  ├─ TRUE → Obter Arquivo → Voz para Texto → Mesclar Texto
  └─ FALSE → (direto)
  ↓
Criar ou Buscar Usuário
  ↓
MCP: Detectar Intenção
  ↓
Roteador de Ação (Switch)
  ├─ INSERT → Extrair → Validar → Formatar → Enviar Confirmação → Aguardar → Verificar → Executar → Enviar Sucesso
  ├─ UPDATE → (similar)
  ├─ DELETE → (similar)
  ├─ LIST → Extrair Filtros → Listar → Formatar → Enviar Lista
  ├─ REPORT → (gerar relatório)
  └─ OTHER → Assistente IA
```

---

## 📚 Documentação Completa

Para mais detalhes, consulte:
- `workflows/N8N_WORKFLOW_GUIDE.md` - Guia completo e detalhado

---

**Fluxo n8n configurado! 🎉**
