# Agente Pessoal - MVP

Sistema inteligente para gerenciar contas a pagar pessoais através do Telegram, utilizando processamento de linguagem natural e servidor MCP.

## 📁 Estrutura do Projeto

```
personal_agent/
├── config/              # Configurações do banco de dados
│   ├── __init__.py
│   └── database.py
├── models/              # Modelos SQLAlchemy
│   ├── __init__.py
│   └── personal_agent_mvp.py
├── services/            # Serviços de negócio
│   ├── __init__.py
│   ├── personal_agent_service.py
│   └── report_service_personal.py
├── mcp_server/          # Servidor MCP FastAPI
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── routers/
│   │   ├── __init__.py
│   │   └── mcp.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── mcp.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── mcp_detector.py
│   │   ├── mcp_extractor.py
│   │   ├── mcp_validator.py
│   │   ├── mcp_lister.py
│   │   └── mcp_formatter.py
│   └── systemd/
│       └── mcp-server.service
├── scripts/             # Scripts SQL
│   └── create_personal_agent_db.sql
├── workflows/           # Documentação do fluxo n8n
│   └── N8N_WORKFLOW_GUIDE.md
├── docs/                # Documentação
│   └── MVP_AGENTE_PESSOAL.md
├── .env.example         # Exemplo de variáveis de ambiente
└── requirements.txt     # Dependências Python
```

## 🚀 Instalação Rápida

### 1. Criar Banco de Dados

```bash
psql -U postgres -f scripts/create_personal_agent_db.sql
```

### 2. Configurar Variáveis de Ambiente

Copie `.env.example` para `.env` e configure:

```env
DATABASE_URL_PERSONAL=postgresql://personal_agent_user:SENHA@localhost:5432/personal_agent_db
MCP_PORT=8001
MCP_HOST=0.0.0.0
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
cd mcp_server
pip install -r requirements.txt
```

### 4. Inicializar Banco

```python
from personal_agent.config.database import init_db_personal
init_db_personal()
```

### 5. Iniciar Servidor MCP

```bash
cd mcp_server
python main.py
```

## 📚 Documentação

- [Documentação Completa](docs/MVP_AGENTE_PESSOAL.md)
- [Guia do Fluxo n8n](workflows/N8N_WORKFLOW_GUIDE.md)

## 🔧 Funcionalidades

- ✅ Cadastro de contas a pagar (texto e voz)
- ✅ Listagem com filtros de período
- ✅ Geração de relatórios
- ✅ Sistema de confirmação obrigatória
- ✅ Validação de dados antes de salvar
- ✅ Suporte a parcelas

## 📝 Exemplos de Uso

**Via Telegram (texto ou voz):**
- "Adicionar conta: Fornecedor XYZ, vencimento 15/01/2025, R$ 1.500"
- "Mostrar minhas contas"
- "Contas de janeiro de 2025"
- "Atualizar conta ID 5: valor R$ 2.000"
- "Excluir conta ID 5"

## 🏗️ Arquitetura

- **Banco de Dados:** PostgreSQL (`personal_agent_db`)
- **Backend:** Python + SQLAlchemy
- **Servidor MCP:** FastAPI
- **Automação:** n8n
- **Integração:** Telegram Bot

## 📦 Dependências

Ver `requirements.txt` e `mcp_server/requirements.txt`
