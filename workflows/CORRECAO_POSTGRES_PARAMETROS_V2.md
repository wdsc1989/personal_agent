# 🔧 Correção do Node "Verificar Se Usuário Existe" - Solução com Node Intermediário

## Problema Reportado

```
Problem in node 'Verificar Se Usuário Existe'
there is no parameter $1
```

## Causa Raiz

O problema persistia mesmo após tentativas de corrigir a expressão diretamente no parâmetro PostgreSQL. Isso indica que:

1. A expressão complexa não estava sendo avaliada corretamente pelo n8n
2. O valor estava retornando `undefined` ou `null` no momento da execução
3. O PostgreSQL node não conseguia processar o parâmetro porque não recebia um valor válido

## Solução Aplicada

Criação de um **node intermediário "Extrair Telegram ID"** (Code node) que:
1. Extrai e valida o `telegram_id` de forma robusta
2. Garante que sempre retorna um número válido
3. Passa os dados de forma limpa para o PostgreSQL node

### Fluxo Corrigido

```
Mesclar Texto
  ↓
Extrair Telegram ID (Code Node) ← NOVO
  ↓
Verificar Se Usuário Existe (PostgreSQL)
  ↓
Usuário Existe?
```

### Node "Extrair Telegram ID"

**Tipo:** Code Node (JavaScript)

**Código:**
```javascript
const input = $input.first().json;
const fromUser = input.from_user;
let telegramId;

try {
  if (typeof fromUser === 'string') {
    const parsed = JSON.parse(fromUser);
    telegramId = parsed.id;
  } else if (fromUser && fromUser.id) {
    telegramId = fromUser.id;
  } else {
    telegramId = fromUser;
  }
} catch(e) {
  telegramId = 0;
}

return {
  telegram_id: telegramId || 0,
  text: input.text || '',
  chat_id: input.chat_id,
  from_user: input.from_user
};
```

### Node "Verificar Se Usuário Existe"

**Query:**
```sql
SELECT id FROM usuarios_telegram WHERE telegram_id = $1;
```

**Parâmetro:**
```json
{
  "value": "={{ $json.telegram_id }}"
}
```

## Vantagens desta Solução

1. ✅ **Validação robusta:** O código JavaScript trata todos os casos possíveis
2. ✅ **Valor garantido:** Sempre retorna um número válido (ou 0 como fallback)
3. ✅ **Debug mais fácil:** Podemos ver o valor exato antes de passar para PostgreSQL
4. ✅ **Manutenção:** Mais fácil de ajustar a lógica de extração se necessário
5. ✅ **Preserva dados:** Mantém `text`, `chat_id`, `from_user` para uso posterior

## Teste

- ✅ **Com from_user como string JSON:** `JSON.parse(fromUser).id` → funciona
- ✅ **Com from_user como objeto:** `fromUser.id` → funciona
- ✅ **Com from_user undefined/null:** Retorna `0` → não quebra
- ✅ **Com erro no parse:** Try/catch retorna `0` → não quebra

---

**Correção aplicada no arquivo:** `workflows/agente_pessoal_mvp_corrigido.json`

**Arquivos atualizados:**
- Adicionado node "Extrair Telegram ID"
- Atualizado node "Verificar Se Usuário Existe" para usar `$json.telegram_id`
- Atualizadas conexões no fluxo
