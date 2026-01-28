# 🔧 Como Corrigir Senha com Caracteres Especiais

## Problema

Se sua senha contém caracteres especiais como `@`, `#`, `$`, etc., eles precisam ser codificados (URL encoded) na string de conexão PostgreSQL.

**Erro comum:**
```
could not translate host name "senha@localhost" to address
```

Isso acontece porque o `@` na senha é interpretado como separador entre credenciais e hostname.

---

## Solução Rápida

### No servidor, execute:

```bash
cd /opt/personal_agent
bash scripts/corrigir_env.sh
```

O script irá:
1. Solicitar a senha
2. Codificar automaticamente
3. Atualizar o arquivo `.env`

---

## Solução Manual

### 1. Codificar a senha manualmente

O caractere `@` deve ser codificado como `%40` na URL.

**Exemplo:**
- Senha original: `n@g3r1995`
- Senha codificada: `n%40g3r1995`
- URL: `postgresql://personal_agent_user:n%40g3r1995@localhost:5432/personal_agent_db`

### 2. Editar arquivo .env

```bash
cd /opt/personal_agent
nano .env
```

Altere a linha:
```env
DATABASE_URL_PERSONAL=postgresql://personal_agent_user:n%40g3r1995@localhost:5432/personal_agent_db
```

### 3. Testar conexão

```bash
python3 scripts/test_connection.py
```

---

## Caracteres Especiais Comuns

| Caractere | Codificação |
|-----------|-------------|
| `@` | `%40` |
| `#` | `%23` |
| `$` | `%24` |
| `%` | `%25` |
| `&` | `%26` |
| `+` | `%2B` |
| `/` | `%2F` |
| `:` | `%3A` |
| `=` | `%3D` |
| `?` | `%3F` |

---

## Verificar se está correto

```bash
# Ver conteúdo do .env
cat .env | grep DATABASE_URL_PERSONAL

# Testar conexão
python3 scripts/test_connection.py
```

Se a conexão funcionar, está correto! ✅

---

## Script Atualizado

O script `deploy_completo.sh` foi atualizado para codificar automaticamente a senha quando você a digita. Isso resolve o problema para futuros deploys.

---

**Problema resolvido! 🎉**
