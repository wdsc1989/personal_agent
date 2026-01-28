# ⚠️ Nota sobre Tratamento de Erros no n8n

## Nodes que podem aparecer "soltos"

Alguns nodes podem aparecer sem conexões visíveis no n8n, mas isso é normal:

### Nodes Finais (sem saída)

Estes nodes são finais e não precisam de conexões de saída:
- **Enviar Resposta Assistente** - Final do fluxo do Assistente IA
- **Enviar Cancelamento** - Final quando operação é cancelada
- **Enviar Sucesso** - Final quando operação é bem-sucedida
- **Enviar Erro** - Final do tratamento de erros

### Tratamento de Erros

O node **"Tratar Erro"** precisa ser conectado manualmente através da configuração "On Error" nos nodes que podem gerar erro.

**Como configurar:**

1. Clique em qualquer node que pode gerar erro (ex: HTTP Request, PostgreSQL, etc.)
2. Vá em **"Settings"** ou **"Options"**
3. Ative **"Continue On Fail"** ou configure **"On Error"**
4. Conecte ao node **"Tratar Erro"**

**Nodes que devem ter tratamento de erro:**
- MCP: Detectar Intenção
- MCP: Extrair Dados
- MCP: Validar Dados
- MCP: Formatar Confirmação
- Executar Inserção
- MCP: Listar Contas
- Criar ou Buscar Usuário

---

## Solução Rápida

Após importar o JSON:

1. **Para nodes finais:** Eles estão corretos, não precisam de conexões de saída
2. **Para tratamento de erros:** Configure manualmente "On Error" nos nodes críticos apontando para "Tratar Erro"

---

**Isso é normal no n8n! Os nodes finais não precisam ter conexões de saída.** ✅
