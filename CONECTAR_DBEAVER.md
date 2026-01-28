# 🔌 Conectar ao PostgreSQL via DBeaver (Acesso Externo)

## Objetivo

Configurar o PostgreSQL para aceitar conexões externas e conectar via DBeaver.

---

## ⚠️ Pré-requisitos

- PostgreSQL rodando no servidor
- Acesso SSH ao servidor
- DBeaver instalado no seu computador
- Porta 5432 aberta no firewall (já está aberta segundo logs anteriores)

---

## 📋 Passo 1: Configurar PostgreSQL para Aceitar Conexões Externas

### 1.1 Editar postgresql.conf

Execute no servidor:

```bash
sudo nano /etc/postgresql/16/main/postgresql.conf
```

**Localize a linha:**
```conf
#listen_addresses = '*'
```

**Descomente e certifique-se que está assim:**
```conf
listen_addresses = '*'
```

**Salvar:** `Ctrl+O`, `Enter`, `Ctrl+X`

### 1.2 Editar pg_hba.conf

```bash
sudo nano /etc/postgresql/16/main/pg_hba.conf
```

**Adicione no final do arquivo (antes das linhas de comentário):**

```conf
# Conexões externas para personal_agent_user
host    personal_agent_db    personal_agent_user    0.0.0.0/0    scram-sha-256
```

**OU se quiser permitir apenas do seu IP específico:**

```conf
# Conexões externas para personal_agent_user (apenas do seu IP)
host    personal_agent_db    personal_agent_user    SEU_IP_AQUI/32    scram-sha-256
```

**Salvar:** `Ctrl+O`, `Enter`, `Ctrl+X`

### 1.3 Reiniciar PostgreSQL

```bash
sudo systemctl restart postgresql
sudo systemctl status postgresql
```

### 1.4 Verificar se está escutando em todas as interfaces

```bash
sudo netstat -tlnp | grep 5432
```

**Deve mostrar:**
```
tcp  0  0  0.0.0.0:5432  0.0.0.0:*  LISTEN  PID/postgres
```

Se mostrar apenas `127.0.0.1:5432`, o `listen_addresses` não foi aplicado corretamente.

---

## 📋 Passo 2: Verificar Firewall

A porta 5432 já está aberta segundo os logs anteriores, mas verifique:

```bash
sudo ufw status
```

**Deve mostrar:**
```
5432/tcp  ALLOW  Anywhere
```

Se não estiver, abra:

```bash
sudo ufw allow 5432/tcp
sudo ufw reload
```

---

## 📋 Passo 3: Configurar DBeaver

### 3.1 Criar Nova Conexão

1. Abra o DBeaver
2. Clique em **"Nova Conexão"** (ícone de plug) ou `Ctrl+Shift+N`
3. Selecione **PostgreSQL**
4. Clique em **"Avançar"**

### 3.2 Configurar Conexão

**Aba "Principal":**

- **Host:** `srv1140258.hstgr.cloud`
- **Porta:** `5432`
- **Database:** `personal_agent_db`
- **Usuário:** `personal_agent_user`
- **Senha:** `Wc153624` (ou a senha que você configurou)

**Aba "SSL" (opcional):**

- Marque **"Use SSL"** se quiser conexão criptografada
- Modo: **"prefer"** ou **"require"**

### 3.3 Testar Conexão

1. Clique em **"Testar Conexão"**
2. Se pedir para baixar driver, clique em **"Baixar"**
3. Aguarde o download e teste novamente

### 3.4 Salvar e Conectar

1. Clique em **"Finalizar"**
2. A conexão aparecerá na lista
3. Clique duas vezes para conectar

---

## 🔧 Configuração Completa do pg_hba.conf

**Exemplo completo do arquivo:**

```conf
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     peer

# IPv4 local connections:
host    all             all             127.0.0.1/32            scram-sha-256

# IPv6 local connections:
host    all             all             ::1/128                 scram-sha-256

# Conexões externas para personal_agent_db
host    personal_agent_db    personal_agent_user    0.0.0.0/0    scram-sha-256

# Allow replication connections from localhost
local   replication     all                                     peer
host    replication     all             127.0.0.1/32            scram-sha-256
host    replication     all             ::1/128                 scram-sha-256
```

---

## 🔒 Segurança (Recomendado)

### Opção 1: Permitir apenas do seu IP

No `pg_hba.conf`, ao invés de `0.0.0.0/0`, use seu IP específico:

```conf
host    personal_agent_db    personal_agent_user    SEU_IP_AQUI/32    scram-sha-256
```

**Para descobrir seu IP:**
- Acesse: https://whatismyipaddress.com/
- Ou use: `curl ifconfig.me`

### Opção 2: Usar túnel SSH (Mais Seguro)

No DBeaver, configure um túnel SSH:

1. Na configuração da conexão, vá na aba **"SSH"**
2. Marque **"Use SSH Tunnel"**
3. Configure:
   - **Host:** `srv1140258.hstgr.cloud`
   - **Porta:** `22`
   - **Usuário:** `root` (ou seu usuário SSH)
   - **Autenticação:** Chave privada ou senha
4. Na aba **"Principal"**, use:
   - **Host:** `localhost` (não o hostname externo)
   - **Porta:** `5432`

Isso cria um túnel seguro através do SSH.

---

## 🧪 Testar Conexão Manualmente

Antes de usar o DBeaver, teste via linha de comando:

```bash
# Do seu computador (se tiver psql instalado)
psql -h srv1140258.hstgr.cloud -p 5432 -U personal_agent_user -d personal_agent_db
```

Ou via telnet (para verificar se a porta está acessível):

```bash
telnet srv1140258.hstgr.cloud 5432
```

---

## 🆘 Troubleshooting

### Erro: "Connection refused"

**Causa:** PostgreSQL não está escutando em todas as interfaces.

**Solução:**
1. Verifique `listen_addresses = '*'` no `postgresql.conf`
2. Reinicie PostgreSQL: `sudo systemctl restart postgresql`
3. Verifique: `sudo netstat -tlnp | grep 5432`

### Erro: "Password authentication failed"

**Causa:** Senha incorreta ou usuário não tem permissão.

**Solução:**
1. Verifique a senha: `sudo -u postgres psql -c "\du personal_agent_user"`
2. Redefina a senha se necessário
3. Verifique o `pg_hba.conf`

### Erro: "No route to host" ou timeout

**Causa:** Firewall bloqueando ou porta não acessível.

**Solução:**
1. Verifique firewall: `sudo ufw status`
2. Abra a porta: `sudo ufw allow 5432/tcp`
3. Verifique se o provedor (Hostinger) não está bloqueando

### Erro: "FATAL: no pg_hba.conf entry"

**Causa:** IP não está na lista de hosts permitidos.

**Solução:**
1. Adicione seu IP no `pg_hba.conf`
2. Ou use `0.0.0.0/0` para permitir de qualquer lugar (menos seguro)
3. Reinicie PostgreSQL

---

## ✅ Checklist

- [ ] `listen_addresses = '*'` configurado no `postgresql.conf`
- [ ] Regra adicionada no `pg_hba.conf` para `personal_agent_user`
- [ ] PostgreSQL reiniciado
- [ ] Porta 5432 aberta no firewall
- [ ] PostgreSQL escutando em `0.0.0.0:5432`
- [ ] Conexão testada no DBeaver

---

## 📝 Resumo dos Dados para DBeaver

- **Host:** `srv1140258.hstgr.cloud`
- **Porta:** `5432`
- **Database:** `personal_agent_db`
- **Usuário:** `personal_agent_user`
- **Senha:** `Wc153624` (ou a que você configurou)

---

**Após configurar, você poderá conectar ao banco via DBeaver! 🎉**
