# 🔧 Corrigir Senha do PostgreSQL

## Problema

Erro: `password authentication failed for user "personal_agent_user"`

Isso significa que a senha no arquivo `.env` não corresponde à senha do usuário no PostgreSQL.

---

## Solução: Redefinir Senha do Usuário

### Opção 1: Redefinir Senha no PostgreSQL (Recomendado)

Execute no servidor:

```bash
# 1. Conectar ao PostgreSQL como superusuário
sudo -u postgres psql

# 2. No psql, redefinir a senha do usuário
ALTER USER personal_agent_user WITH PASSWORD 'SUA_NOVA_SENHA_AQUI';

# 3. Verificar se funcionou
\du personal_agent_user

# 4. Sair do psql
\q
```

### Opção 2: Atualizar .env com a Senha Correta

Se você sabe qual é a senha correta do usuário no PostgreSQL:

```bash
cd /opt/personal_agent
nano .env
```

Edite a linha:
```env
DATABASE_URL_PERSONAL=postgresql://personal_agent_user:SENHA_CORRETA@localhost:5432/personal_agent_db
```

Salve: `Ctrl+O`, `Enter`, `Ctrl+X`

---

## Passo a Passo Completo

### 1. Verificar se o usuário existe

```bash
sudo -u postgres psql -c "\du personal_agent_user"
```

### 2. Redefinir senha no PostgreSQL

```bash
sudo -u postgres psql << EOF
ALTER USER personal_agent_user WITH PASSWORD 'SUA_NOVA_SENHA_AQUI';
\q
EOF
```

**IMPORTANTE:** Substitua `SUA_NOVA_SENHA_AQUI` pela senha que você quer usar.

### 3. Atualizar .env com a mesma senha

```bash
cd /opt/personal_agent
nano .env
```

Edite:
```env
DATABASE_URL_PERSONAL=postgresql://personal_agent_user:SUA_NOVA_SENHA_AQUI@localhost:5432/personal_agent_db
```

Salve: `Ctrl+O`, `Enter`, `Ctrl+X`

### 4. Testar conexão

```bash
cd /opt/personal_agent
source venv/bin/activate
python3 scripts/test_connection.py
```

---

## Verificar Senha Atual (se esquecer)

Se você não lembra qual senha está configurada no PostgreSQL, você precisa redefini-la:

```bash
sudo -u postgres psql
ALTER USER personal_agent_user WITH PASSWORD 'nova_senha_segura';
\q
```

Depois atualize o `.env` com a mesma senha.

---

## Testar Conexão Manual

Para testar se a senha está correta:

```bash
psql -U personal_agent_user -d personal_agent_db -h localhost
```

Se pedir senha e aceitar, a senha está correta. Se der erro, a senha está errada.

---

## Comandos Rápidos (Tudo de Uma Vez)

```bash
# Definir nova senha (escolha uma senha segura)
NOVA_SENHA="sua_senha_segura_aqui"

# Redefinir no PostgreSQL
sudo -u postgres psql -c "ALTER USER personal_agent_user WITH PASSWORD '$NOVA_SENHA';"

# Atualizar .env
cd /opt/personal_agent
sed -i "s|postgresql://personal_agent_user:[^@]*@|postgresql://personal_agent_user:$NOVA_SENHA@|g" .env

# Testar
source venv/bin/activate
python3 scripts/test_connection.py
```

---

## Importante

- A senha no PostgreSQL e no `.env` devem ser **exatamente iguais**
- Use `localhost` como host (não o hostname externo)
- Se a senha tiver caracteres especiais, codifique-os na URL:
  - `@` → `%40`
  - `#` → `%23`
  - `$` → `%24`

---

**Após corrigir, teste novamente com `python3 scripts/test_connection.py`**
