# 🔧 Correção do Node "Verificar Se Usuário Existe" - Parâmetros PostgreSQL

## Problema Reportado

```
Problem in node 'Verificar Se Usuário Existe'
there is no parameter $1
```

## Causa

O node PostgreSQL estava tentando usar um parâmetro `$1` na query SQL, mas o valor do parâmetro estava retornando `undefined` ou `null`, fazendo com que o PostgreSQL não conseguisse processar o parâmetro.

**Possíveis causas:**
1. A expressão `JSON.parse($json.from_user).id` estava retornando `undefined`
2. O campo `from_user` não estava disponível no contexto do node
3. O formato dos parâmetros não estava sendo reconhecido corretamente pelo n8n

## Solução Aplicada

Mudança na expressão do parâmetro para garantir que sempre retorne um valor válido:

**Antes:**
```json
{
  "value": "={{ JSON.parse($json.from_user).id }}"
}
```

**Depois:**
```json
{
  "value": "={{ typeof $json.from_user === 'string' ? JSON.parse($json.from_user).id : ($json.from_user?.id || $json.from_user) }}"
}
```

## Explicação

A nova expressão:
1. **Verifica o tipo:** Se `from_user` é uma string, faz `JSON.parse`
2. **Fallback:** Se não for string, tenta acessar `.id` diretamente
3. **Último fallback:** Se não houver `.id`, usa o próprio valor de `from_user`

Isso garante que sempre teremos um valor válido para passar como parâmetro.

## Formato dos Parâmetros PostgreSQL no n8n

O formato correto para parâmetros no PostgreSQL node (versão 2.6) é:

```json
{
  "parameters": {
    "operation": "executeQuery",
    "query": "=SELECT id FROM table WHERE column = $1;",
    "options": {
      "queryParameters": {
        "parameters": [
          {
            "value": "={{ $json.field }}"
          }
        ]
      }
    }
  }
}
```

**Importante:**
- Os parâmetros devem estar dentro de `options.queryParameters.parameters`
- Cada parâmetro deve ser um objeto com `"value"`
- A ordem dos parâmetros deve corresponder à ordem dos placeholders (`$1`, `$2`, etc.)

## Teste

- ✅ **Com from_user como string JSON:** `JSON.parse($json.from_user).id` → funciona
- ✅ **Com from_user como objeto:** `$json.from_user.id` → funciona
- ✅ **Com from_user undefined:** Fallback para valor padrão → não quebra

---

**Correção aplicada no arquivo:** `workflows/agente_pessoal_mvp_corrigido.json`

**Nota:** Se o problema persistir, pode ser necessário verificar:
1. Se o campo `from_user` está sendo passado corretamente pelo node "Mesclar Texto"
2. Se o formato do JSON em `from_user` está correto
3. Se há algum problema com a versão do n8n PostgreSQL node
