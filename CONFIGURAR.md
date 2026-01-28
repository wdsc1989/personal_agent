# 🚀 Guia de Configuração Rápida

## Opção 1: Configuração Automática (Recomendado)

Execute o script interativo:

```bash
cd personal_agent
python setup_config.py
```

O script irá:
1. ✅ Criar o arquivo `.env` com suas configurações
2. ✅ Testar a conexão com o banco
3. ✅ Inicializar as tabelas

## Opção 2: Configuração Manual

### Passo 1: Criar arquivo .env

Copie o exemplo:

```bash
cd personal_agent
cp .env.example .env
```

Edite o arquivo `.env` e configure:

```env
DATABASE_URL_PERSONAL=postgresql://personal_agent_user:SUA_SENHA@localhost:5432/personal_agent_db
MCP_PORT=8001
MCP_HOST=0.0.0.0
```

**Para servidor Hostinger:**
```env
DATABASE_URL_PERSONAL=postgresql://personal_agent_user:SUA_SENHA@srv1140258.hstgr.cloud:5432/personal_agent_db
```

### Passo 2: Criar banco de dados

Execute o script SQL:

```bash
# No servidor Hostinger
psql -U postgres -f scripts/create_personal_agent_db.sql
```

**IMPORTANTE:** Antes de executar, edite o script e altere `SENHA_SEGURA_AQUI` para uma senha real!

### Passo 3: Testar conexão

```python
from config.database import test_connection_personal
test_connection_personal()
```

### Passo 4: Inicializar tabelas

```python
from config.database import init_db_personal
init_db_personal()
```

### Passo 5: Instalar dependências

```bash
# Dependências principais
pip install -r requirements.txt

# Dependências do servidor MCP
cd mcp_server
pip install -r requirements.txt
```

### Passo 6: Iniciar servidor MCP

```bash
cd mcp_server
python main.py
```

## Verificação

### Testar servidor MCP

```bash
curl http://localhost:8001/health
```

Ou acesse no navegador: `http://localhost:8001`

### Verificar banco de dados

```python
from config.database import test_connection_personal
test_connection_personal()
```

## Próximos Passos

1. Configure o fluxo n8n: `workflows/N8N_WORKFLOW_GUIDE.md`
2. Teste os comandos via Telegram
3. Consulte a documentação: `docs/MVP_AGENTE_PESSOAL.md`

## Troubleshooting

### Erro de conexão

- Verifique se o PostgreSQL está rodando
- Verifique as credenciais no `.env`
- Verifique se o banco foi criado
- Para servidor remoto, verifique firewall/portas

### Erro de import

Execute a partir do diretório `personal_agent/`:

```bash
cd personal_agent
python -m mcp_server.main
```

### Porta já em uso

Altere a porta no `.env`:

```env
MCP_PORT=8002
```
