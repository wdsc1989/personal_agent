# Guia de Setup - Agente Pessoal

## Estrutura do Diretório

Todos os arquivos do agente pessoal foram organizados no diretório `personal_agent/`, separado do sistema contábil (`contabil_system/`).

## Passos de Instalação

### 1. Criar Banco de Dados PostgreSQL

```bash
# Conecte-se ao PostgreSQL como superusuário
psql -U postgres

# Execute o script SQL
\i scripts/create_personal_agent_db.sql
```

Ou execute diretamente:

```bash
psql -U postgres -f scripts/create_personal_agent_db.sql
```

**Importante:** Altere a senha `SENHA_SEGURA_AQUI` no script antes de executar!

### 2. Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` na raiz do diretório `personal_agent/`:

```bash
cd personal_agent
cp .env.example .env
```

Edite o arquivo `.env` e configure:

```env
DATABASE_URL_PERSONAL=postgresql://personal_agent_user:SUA_SENHA_AQUI@localhost:5432/personal_agent_db
MCP_PORT=8001
MCP_HOST=0.0.0.0
```

### 3. Instalar Dependências

#### Dependências principais:

```bash
cd personal_agent
pip install -r requirements.txt
```

#### Dependências do servidor MCP:

```bash
cd personal_agent/mcp_server
pip install -r requirements.txt
```

### 4. Inicializar Banco de Dados

```python
# No diretório personal_agent
python -c "from config.database import init_db_personal; init_db_personal()"
```

Ou crie um script `init_db.py`:

```python
from config.database import init_db_personal

if __name__ == "__main__":
    init_db_personal()
```

Execute:

```bash
python init_db.py
```

### 5. Iniciar Servidor MCP

#### Desenvolvimento:

```bash
cd personal_agent/mcp_server
python main.py
```

O servidor estará disponível em `http://localhost:8001`

#### Produção (systemd):

```bash
# Copiar arquivo de serviço
sudo cp mcp_server/systemd/mcp-server.service /etc/systemd/system/

# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar serviço
sudo systemctl enable mcp-server

# Iniciar serviço
sudo systemctl start mcp-server

# Verificar status
sudo systemctl status mcp-server
```

**Nota:** Ajuste o caminho `WorkingDirectory` no arquivo `.service` conforme necessário.

### 6. Verificar Instalação

#### Testar conexão com banco:

```python
from config.database import test_connection_personal
test_connection_personal()
```

#### Testar servidor MCP:

```bash
curl http://localhost:8001/health
```

Ou acesse no navegador: `http://localhost:8001`

## Configuração do n8n

Siga o guia completo em `workflows/N8N_WORKFLOW_GUIDE.md` para configurar o fluxo no n8n.

**URLs importantes:**
- Servidor MCP: `http://localhost:8001`
- Endpoints: `http://localhost:8001/mcp/*`

## Estrutura de Diretórios

```
personal_agent/
├── config/              # Configuração do banco
├── models/              # Modelos SQLAlchemy
├── services/            # Serviços de negócio
├── mcp_server/          # Servidor MCP FastAPI
├── scripts/             # Scripts SQL
├── workflows/           # Guias do n8n
├── docs/                # Documentação
├── .env                 # Variáveis de ambiente (criar)
├── .env.example         # Exemplo de variáveis
├── requirements.txt     # Dependências principais
└── README.md            # Documentação principal
```

## Troubleshooting

### Erro de import

Se houver erros de import, certifique-se de executar os scripts a partir do diretório `personal_agent/`:

```bash
cd personal_agent
python -m mcp_server.main
```

### Servidor MCP não inicia

1. Verifique se a porta 8001 está disponível
2. Verifique as variáveis de ambiente no `.env`
3. Verifique se o banco de dados está acessível
4. Verifique os logs: `sudo journalctl -u mcp-server -f`

### Erro de conexão com banco

1. Verifique se o PostgreSQL está rodando
2. Verifique as credenciais no `.env`
3. Verifique se o banco `personal_agent_db` foi criado
4. Verifique se o usuário `personal_agent_user` tem permissões

## Próximos Passos

1. Configure o fluxo n8n seguindo `workflows/N8N_WORKFLOW_GUIDE.md`
2. Teste os comandos via Telegram
3. Verifique os logs do servidor MCP
4. Ajuste conforme necessário
