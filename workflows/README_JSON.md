# 📄 JSON do Fluxo n8n - Agente Pessoal MVP

## Arquivo

**`workflows/agente_pessoal_mvp.json`**

Este é o JSON completo do fluxo n8n para a versão **1.122.4**, pronto para importar.

---

## 📋 Como Usar

### 1. Importar no n8n

1. Acesse o n8n
2. Vá em **Workflows** → **Import from File**
3. Selecione o arquivo `agente_pessoal_mvp.json`
4. Clique em **Import**

### 2. Configurar Credenciais

Após importar, configure:

- **Telegram Bot** - Token do seu bot
- **PostgreSQL** - Credenciais do banco `personal_agent_db`
- **OpenAI** - API Key para transcrição de áudio

### 3. Ajustar IDs de Credenciais

Os IDs no JSON são placeholders. Após criar as credenciais:

1. Clique em cada node que usa credenciais
2. Selecione a credencial correta
3. Salve

---

## 🎯 Funcionalidades Incluídas

✅ **Telegram Trigger** - Escuta mensagens de texto e áudio
✅ **Transcrição de Áudio** - Converte voz em texto usando OpenAI
✅ **Integração MCP** - Usa servidor MCP para detecção, extração e validação
✅ **Sistema de Confirmação** - Todas as operações CRUD requerem confirmação
✅ **Criação Automática de Usuário** - Cria usuário Telegram se não existir
✅ **INSERT** - Inserir contas a pagar
✅ **LIST** - Listar contas com filtros
✅ **Validação** - Valida dados antes de salvar
✅ **Tratamento de Erros** - Tratamento robusto de erros
✅ **Assistente IA** - Para quando a ação não é clara

---

## 🔗 Endpoints MCP Utilizados

- `POST http://localhost:8001/mcp/detect` - Detectar intenção
- `POST http://localhost:8001/mcp/extract` - Extrair dados
- `POST http://localhost:8001/mcp/validate` - Validar dados
- `POST http://localhost:8001/mcp/list` - Listar contas
- `POST http://localhost:8001/mcp/format-confirmation` - Formatar confirmação

---

## 📝 Nodes Incluídos

1. **Escutar Mensagens** - Telegram Trigger
2. **Preparar Dados** - Set node
3. **É Áudio?** - IF node
4. **Obter Arquivo de Voz** - Telegram Get File
5. **Voz para Texto** - OpenAI Transcribe
6. **Mesclar Texto** - Set node
7. **Criar ou Buscar Usuário** - PostgreSQL
8. **MCP: Detectar Intenção** - HTTP Request
9. **Roteador de Ação** - Switch node
10. **MCP: Extrair Dados** - HTTP Request
11. **MCP: Validar Dados** - HTTP Request
12. **Verificar Validação** - IF node
13. **MCP: Formatar Confirmação** - HTTP Request
14. **Enviar Confirmação** - Telegram Send Message
15. **Aguardar Confirmação** - Wait node
16. **Aguardar Resposta** - Telegram Trigger
17. **Verificar Confirmação** - Code node
18. **Executar ou Cancelar** - Switch node
19. **Executar Inserção** - PostgreSQL
20. **Enviar Sucesso** - Telegram Send Message
21. **MCP: Extrair Filtros** - HTTP Request (para LIST)
22. **MCP: Listar Contas** - HTTP Request
23. **Formatar Lista** - Code node
24. **Enviar Lista** - Telegram Send Message
25. **Assistente IA** - OpenAI Chat (para OTHER)
26. **Enviar Resposta Assistente** - Telegram Send Message
27. **Tratar Erro** - Code node
28. **Enviar Erro** - Telegram Send Message

---

## ⚠️ Ajustes Necessários Após Importar

1. **Credenciais:** Configure todas as credenciais (Telegram, PostgreSQL, OpenAI)
2. **Webhook IDs:** Podem precisar ser regenerados
3. **URLs MCP:** Verifique se `localhost:8001` está correto
4. **Parâmetros PostgreSQL:** Verifique se os parâmetros estão sendo passados corretamente

---

## 🧪 Testar

Após importar e configurar:

1. Ative o workflow
2. Envie mensagem de teste:
   ```
   Adicionar conta: Fornecedor XYZ, vencimento 15/01/2025, R$ 1.500
   ```
3. Verifique se o fluxo executa corretamente

---

## 📚 Documentação Relacionada

- `N8N_WORKFLOW_GUIDE.md` - Guia completo e detalhado
- `INSTRUCOES_IMPORTAR_JSON.md` - Instruções de importação
- `CONFIGURAR_N8N.md` - Guia prático de configuração

---

**JSON pronto para importar! 🚀**
