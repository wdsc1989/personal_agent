# 📥 Como Importar o JSON do Fluxo n8n

## Arquivo

O arquivo JSON completo está em: `workflows/agente_pessoal_mvp.json`

---

## 📋 Passo a Passo para Importar

### 1. Acessar n8n

1. Acesse o n8n no servidor
2. Faça login

### 2. Importar Workflow

1. Clique em **"Workflows"** no menu lateral
2. Clique no botão **"Import from File"** ou **"Import"**
3. Selecione o arquivo: `workflows/agente_pessoal_mvp.json`
4. Clique em **"Import"**

### 3. Configurar Credenciais

Após importar, você precisará configurar as credenciais:

#### 3.1 Telegram Bot

1. Clique em qualquer node do Telegram
2. Clique em **"Create New Credential"** ou selecione existente
3. Configure:
   - **Bot Token:** Token do seu bot Telegram
   - Salve

#### 3.2 PostgreSQL

1. Clique no node "Criar ou Buscar Usuário" ou "Executar Inserção"
2. Clique em **"Create New Credential"** ou selecione existente
3. Configure:
   - **Host:** `localhost`
   - **Porta:** `5432`
   - **Database:** `personal_agent_db`
   - **Usuário:** `personal_agent_user`
   - **Senha:** `Wc153624` (ou a senha configurada)
   - Salve

#### 3.3 OpenAI (para transcrição de áudio)

1. Clique no node "Voz para Texto"
2. Clique em **"Create New Credential"** ou selecione existente
3. Configure:
   - **API Key:** Sua chave da OpenAI
   - Salve

---

## ⚠️ Ajustes Necessários Após Importar

### 1. IDs de Credenciais

Os IDs de credenciais no JSON são placeholders. Após criar as credenciais no n8n:

1. Anote os IDs reais das credenciais criadas
2. Ou simplesmente reconfigure cada node para usar as credenciais corretas

### 2. Webhook IDs

Os webhook IDs podem precisar ser regenerados:

1. Clique no node "Escutar Mensagens"
2. Verifique se o webhook está ativo
3. Se necessário, clique em "Listen for Test Event" para gerar novo webhook

### 3. Verificar URLs do MCP

Certifique-se de que as URLs estão corretas:
- `http://localhost:8001/mcp/detect`
- `http://localhost:8001/mcp/extract`
- `http://localhost:8001/mcp/validate`
- `http://localhost:8001/mcp/list`
- `http://localhost:8001/mcp/format-confirmation`

Se o n8n estiver em outro servidor, altere `localhost` para o IP/hostname correto.

---

## 🧪 Testar Após Importar

1. Ative o workflow (toggle no canto superior direito)
2. Envie uma mensagem de teste via Telegram:
   ```
   Adicionar conta: Fornecedor XYZ, vencimento 15/01/2025, R$ 1.500
   ```
3. Verifique se o fluxo executa corretamente

---

## 🔧 Correções Comuns

### Erro: "Credential not found"

- Crie as credenciais necessárias
- Reconecte os nodes às credenciais corretas

### Erro: "Connection refused" no MCP

- Verifique se o servidor MCP está rodando: `curl http://localhost:8001/health`
- Verifique as URLs nos nodes HTTP Request

### Erro: "Database connection failed"

- Verifique credenciais do PostgreSQL
- Teste conexão: `python3 scripts/test_connection.py`

### Erro: "Webhook not active"

- Ative o workflow
- Verifique se o webhook do Telegram está configurado corretamente

---

## 📝 Notas

- O JSON foi criado para n8n versão 1.122.4
- Todos os nomes de nodes estão em português
- O fluxo inclui sistema completo de confirmação
- Suporta texto e áudio (transcrição)

---

**Após importar e configurar, o fluxo estará pronto para uso! 🚀**
