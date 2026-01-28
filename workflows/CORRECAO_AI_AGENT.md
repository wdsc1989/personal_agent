# 🔧 Correção: Uso do AI Agent no n8n

## Problema Identificado

Os nodes de IA estavam usando `@n8n/n8n-nodes-langchain.lmChatOpenAi`, que não funciona corretamente no n8n versão 1.122.4 para criar conexões no fluxo.

## Solução

Substituído por `@n8n/n8n-nodes-langchain.agent` (AI Agent node).

---

## Mudanças Realizadas

### 1. Agente: Orientar Novo Usuário

**Antes:**
```json
{
  "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
  "typeVersion": 1,
  "parameters": {
    "model": "gpt-4o-mini",
    "messages": { ... }
  }
}
```

**Depois:**
```json
{
  "type": "@n8n/n8n-nodes-langchain.agent",
  "typeVersion": 3,
  "parameters": {
    "promptType": "define",
    "text": "={{ ... }}",
    "options": {
      "systemMessage": "=..."
    }
  }
}
```

**Formato Mínimo (conforme exemplo do n8n):**
```json
{
  "type": "@n8n/n8n-nodes-langchain.agent",
  "typeVersion": 3,
  "parameters": {
    "promptType": "define",
    "options": {}
  }
}
```

> **Nota:** O formato mínimo acima é usado quando o prompt é definido diretamente na interface do n8n. No JSON exportado, mantemos `text` e `systemMessage` para que funcione ao importar.

### 2. Assistente IA

Mesma correção aplicada.

---

## Formato do AI Agent Node

### Parâmetros Principais

- **agent**: `"openAi"` - Tipo de agente
- **promptType**: `"define"` - Tipo de prompt
- **text**: Expressão n8n com o texto de entrada
- **options.systemMessage**: Mensagem do sistema (prompt)

### Saída do Node

O AI Agent retorna:
```json
{
  "output": "Resposta do agente"
}
```

Por isso, nos nodes seguintes usamos: `{{ $json.output }}`

---

## Verificação das Conexões

Após importar, verifique se:

1. ✅ **Agente: Orientar Novo Usuário** está conectado corretamente:
   - Entrada: De "Usuário Existe?" (FALSE)
   - Saída: Para "Enviar Orientação"

2. ✅ **Assistente IA** está conectado corretamente:
   - Entrada: De "Roteador de Ação" (OTHER)
   - Saída: Para "Enviar Resposta Assistente"

---

## Se Ainda Não Funcionar

Se após importar os nodes ainda aparecerem "soltos":

1. **Verifique o tipo do node:**
   - Deve ser: `@n8n/n8n-nodes-langchain.agent`
   - Não deve ser: `lmChatOpenAi` ou `lmChat`

2. **Reconecte manualmente:**
   - Clique no node AI Agent
   - Arraste a conexão para o node seguinte
   - Salve

3. **Verifique a versão:**
   - `typeVersion` deve ser `3` (versão correta para n8n 1.122.4)

---

## Arquivo Atualizado

**`workflows/agente_pessoal_mvp_atualizado.json`**

- ✅ 2 nodes AI Agent configurados corretamente
- ✅ Conexões definidas no JSON
- ✅ Formato compatível com n8n 1.122.4

---

**Correção aplicada! Os agentes agora devem aparecer conectados corretamente.** ✅
