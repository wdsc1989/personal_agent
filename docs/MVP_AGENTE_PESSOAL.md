# Documentação MVP - Agente Pessoal

## Visão Geral

O Agente Pessoal MVP é um sistema inteligente que permite gerenciar contas a pagar pessoais através do Telegram, utilizando processamento de linguagem natural (NLP) e um servidor MCP (Model Context Protocol) para detecção, extração e validação de dados.

## Arquitetura

### Componentes Principais

1. **Banco de Dados PostgreSQL** (`personal_agent_db`)
   - Separado do banco contábil
   - Tabelas com colunas em português
   - Usuários do Telegram e contas a pagar

2. **Servidor MCP (FastAPI)**
   - Endpoints para detecção, extração, validação e listagem
   - Processamento de linguagem natural
   - Validação de dados antes de salvar

3. **Fluxo n8n**
   - Integração com Telegram
   - Processamento de texto e áudio
   - Sistema de confirmação obrigatória
   - Execução de operações no banco

## Estrutura do Banco de Dados

### Tabela: `usuarios_telegram`

Armazena informações dos usuários do Telegram.

**Campos:**
- `id` (PK)
- `telegram_id` (BIGINT, UNIQUE)
- `nome_usuario` (VARCHAR)
- `primeiro_nome` (VARCHAR)
- `ultimo_nome` (VARCHAR)
- `telefone` (VARCHAR)
- `codigo_idioma` (VARCHAR, default: 'pt-BR')
- `preferencias` (JSONB)
- `criado_em` (TIMESTAMP)
- `ultimo_acesso` (TIMESTAMP)
- `ativo` (BOOLEAN)

### Tabela: `contas_pagar`

Armazena contas a pagar pessoais.

**Campos:**
- `id` (PK)
- `usuario_telegram_id` (FK → usuarios_telegram.id)
- `nome_credor` (VARCHAR, NOT NULL)
- `descricao` (TEXT)
- `valor_total` (DECIMAL, NOT NULL)
- `valor_pago` (DECIMAL, default: 0)
- `data_vencimento` (DATE, NOT NULL)
- `data_pagamento` (DATE)
- `numero_parcelas` (INTEGER)
- `parcela_atual` (INTEGER)
- `status` (VARCHAR, default: 'pendente')
- `categoria` (VARCHAR)
- `observacoes` (TEXT)
- `criado_em` (TIMESTAMP)
- `atualizado_em` (TIMESTAMP)

## Servidor MCP

### Endpoints

#### POST `/mcp/detect`

Detecta a intenção do usuário a partir do texto.

**Request:**
```json
{
  "text": "Adicionar conta: Fornecedor XYZ, vencimento 15/01/2025, R$ 1.500",
  "context": {}
}
```

**Response:**
```json
{
  "action": "INSERT",
  "entity": "contas_pagar",
  "confidence": 0.9,
  "extracted_info": {}
}
```

#### POST `/mcp/extract`

Extrai dados estruturados do texto.

**Request:**
```json
{
  "text": "Adicionar conta: Fornecedor XYZ, vencimento 15/01/2025, R$ 1.500",
  "action": "INSERT",
  "context": {}
}
```

**Response:**
```json
{
  "data": {
    "nome_credor": "Fornecedor XYZ",
    "valor_total": 1500.0,
    "data_vencimento": "2025-01-15"
  },
  "confidence": 0.9,
  "missing_fields": []
}
```

#### POST `/mcp/validate`

Valida dados antes de salvar.

**Request:**
```json
{
  "data": {
    "nome_credor": "Fornecedor XYZ",
    "valor_total": 1500.0,
    "data_vencimento": "2025-01-15"
  },
  "action": "INSERT"
}
```

**Response:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": []
}
```

#### POST `/mcp/list`

Lista contas com filtros.

**Request:**
```json
{
  "usuario_telegram_id": 123456789,
  "data_inicial": "2025-01-01",
  "data_final": "2025-01-31",
  "status": "pendente",
  "categoria": null
}
```

**Response:**
```json
{
  "contas": [
    {
      "id": 1,
      "nome_credor": "Fornecedor XYZ",
      "valor_total": 1500.0,
      "data_vencimento": "2025-01-15",
      "status": "pendente"
    }
  ],
  "total": 1,
  "total_valor": 1500.0
}
```

#### POST `/mcp/format-confirmation`

Formata mensagem de confirmação.

**Request:**
```json
{
  "action": "INSERT",
  "data": {
    "nome_credor": "Fornecedor XYZ",
    "valor_total": 1500.0,
    "data_vencimento": "2025-01-15"
  },
  "old_data": null
}
```

**Response:**
```json
{
  "message": "📝 **Nova Conta a Pagar**\n\nConfirme os dados...",
  "preview": {
    "nome_credor": "Fornecedor XYZ",
    "valor_total": 1500.0,
    "data_vencimento": "2025-01-15"
  }
}
```

## Instalação

### 1. Criar Banco de Dados

Execute o script SQL:

```bash
psql -U postgres -f scripts/create_personal_agent_db.sql
```

### 2. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL_PERSONAL=postgresql://personal_agent_user:SENHA_SEGURA@localhost:5432/personal_agent_db
MCP_PORT=8001
MCP_HOST=0.0.0.0
```

### 3. Instalar Dependências do Servidor MCP

```bash
cd mcp_server
pip install -r requirements.txt
```

### 4. Inicializar Banco de Dados

```python
from personal_agent.config.database import init_db_personal
init_db_personal()
```

### 5. Iniciar Servidor MCP

```bash
cd mcp_server
python main.py
```

Ou usando systemd:

```bash
sudo cp mcp_server/systemd/mcp-server.service /etc/systemd/system/
sudo systemctl enable mcp-server
sudo systemctl start mcp-server
```

### 6. Configurar Fluxo n8n

Importe o fluxo seguindo o guia em `workflows/N8N_WORKFLOW_GUIDE.md`.

## Uso

### Comandos de Texto

- **Inserir conta:** "Adicionar conta: Fornecedor XYZ, vencimento 15/01/2025, R$ 1.500"
- **Listar contas:** "Mostrar minhas contas"
- **Listar por período:** "Contas de janeiro de 2025"
- **Atualizar conta:** "Atualizar conta ID 5: valor R$ 2.000"
- **Deletar conta:** "Excluir conta ID 5"

### Comandos de Voz

Envie uma mensagem de áudio pelo Telegram com o mesmo conteúdo dos comandos de texto. O sistema transcreverá automaticamente e processará.

## Sistema de Confirmação

Todas as operações CRUD (INSERT, UPDATE, DELETE) requerem confirmação explícita do usuário:

1. Sistema detecta ação e extrai dados
2. Valida dados
3. Envia preview formatado
4. Aguarda confirmação (SIM/NÃO)
5. Executa ou cancela operação

## Funcionalidades

### Cadastro de Contas

- Extração automática de dados do texto/áudio
- Validação antes de salvar
- Confirmação obrigatória
- Suporte a parcelas

### Listagem

- Listagem geral
- Filtro por período
- Filtro por status
- Filtro por categoria
- Combinação de filtros

### Relatórios

- Resumo mensal
- Por categoria
- Contas vencidas
- Previsão mensal

## Próximas Fases

- Lembretes inteligentes
- Anotações de reuniões
- Action items
- Tags personalizadas
- Contas a receber
- Integrações externas

## Troubleshooting

### Servidor MCP não inicia

Verifique:
- Porta 8001 disponível
- Variáveis de ambiente configuradas
- Dependências instaladas
- Banco de dados acessível

### Erro de conexão com banco

Verifique:
- Credenciais corretas
- Banco criado
- Usuário com permissões
- PostgreSQL rodando

### Fluxo n8n não funciona

Verifique:
- Servidor MCP rodando
- Credenciais do Telegram configuradas
- Credenciais do PostgreSQL configuradas
- URLs corretas nos nodes HTTP Request

## Suporte

Para mais informações, consulte:
- `workflows/N8N_WORKFLOW_GUIDE.md` - Guia do fluxo n8n
- `scripts/create_personal_agent_db.sql` - Script de criação do banco
- `mcp_server/` - Código do servidor MCP
