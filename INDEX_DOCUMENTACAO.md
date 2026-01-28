# 📚 Índice de Documentação - Agente Pessoal

## 🚀 Guias de Deploy

### Para Deploy Completo:
1. **`DEPLOY_COMPLETO.md`** ⭐
   - Guia completo passo a passo
   - Do setup local até deploy no servidor
   - Troubleshooting incluído

2. **`RESUMO_DEPLOY.md`**
   - Resumo rápido do processo
   - Checklist de verificação
   - Comandos essenciais

3. **`COMANDOS_DEPLOY.txt`**
   - Comandos prontos para copiar/colar
   - Ordem sequencial de execução
   - Comentários explicativos

### Para Configuração Inicial:
4. **`SETUP.md`**
   - Guia de setup detalhado
   - Instalação de dependências
   - Configuração inicial

5. **`CONFIGURAR.md`**
   - Guia de configuração rápida
   - Opções automática e manual
   - Troubleshooting

6. **`PROXIMOS_PASSOS.md`**
   - Próximos passos após configuração
   - Checklist de verificação
   - Links para documentação

---

## 📖 Documentação Técnica

7. **`docs/MVP_AGENTE_PESSOAL.md`**
   - Documentação completa do MVP
   - Arquitetura do sistema
   - Endpoints da API
   - Exemplos de uso

8. **`workflows/N8N_WORKFLOW_GUIDE.md`**
   - Guia completo do fluxo n8n
   - Configuração de cada node
   - Exemplos de comandos
   - Sistema de confirmação

9. **`README.md`**
   - Visão geral do projeto
   - Estrutura de diretórios
   - Instalação rápida

---

## 🛠️ Scripts e Ferramentas

### Scripts de Deploy:
- **`scripts/deploy_servidor.sh`**
  - Script automático de deploy
  - Executa todos os passos necessários
  - Para usar no servidor

### Scripts de Configuração:
- **`scripts/create_personal_agent_db.sql`**
  - Script SQL para criar banco
  - Cria usuário, banco e tabelas
  - **IMPORTANTE:** Editar senha antes de usar!

- **`scripts/init_tables.py`**
  - Inicializa tabelas do banco
  - Testa conexão antes de criar
  - Executar após criar o banco

- **`scripts/test_connection.py`**
  - Testa conexão com banco
  - Verifica credenciais
  - Útil para troubleshooting

### Scripts Locais:
- **`setup_config.py`**
  - Configuração interativa
  - Cria arquivo .env
  - Testa conexão

- **`criar_env.py`**
  - Cria .env rapidamente
  - Valores padrão para Hostinger
  - Pode receber senha como argumento

---

## 📁 Estrutura de Arquivos

```
personal_agent/
├── 📄 README.md                    # Visão geral
├── 📄 RESUMO_DEPLOY.md             # Resumo rápido deploy
├── 📄 DEPLOY_COMPLETO.md           # Guia completo deploy ⭐
├── 📄 COMANDOS_DEPLOY.txt          # Comandos prontos
├── 📄 SETUP.md                      # Guia de setup
├── 📄 CONFIGURAR.md                 # Configuração
├── 📄 PROXIMOS_PASSOS.md            # Próximos passos
├── 📄 INDEX_DOCUMENTACAO.md         # Este arquivo
│
├── 📄 .env                          # Configurações (criar)
├── 📄 .env.example                 # Exemplo de .env
├── 📄 requirements.txt              # Dependências Python
│
├── 📁 config/                       # Configurações
│   └── database.py                 # Configuração do banco
│
├── 📁 models/                       # Modelos SQLAlchemy
│   └── personal_agent_mvp.py       # Modelos do MVP
│
├── 📁 services/                     # Serviços de negócio
│   ├── personal_agent_service.py   # CRUD de contas
│   └── report_service_personal.py  # Relatórios
│
├── 📁 mcp_server/                   # Servidor MCP FastAPI
│   ├── main.py                     # Aplicação principal
│   ├── config.py                   # Configurações MCP
│   ├── requirements.txt            # Dependências MCP
│   ├── routers/                    # Rotas da API
│   ├── schemas/                    # Schemas Pydantic
│   ├── services/                   # Serviços MCP
│   └── systemd/                    # Configuração systemd
│       └── mcp-server.service      # Serviço systemd
│
├── 📁 scripts/                       # Scripts utilitários
│   ├── create_personal_agent_db.sql # SQL para criar banco
│   ├── deploy_servidor.sh          # Script de deploy
│   ├── init_tables.py              # Inicializar tabelas
│   └── test_connection.py          # Testar conexão
│
├── 📁 workflows/                     # Documentação n8n
│   └── N8N_WORKFLOW_GUIDE.md       # Guia do fluxo n8n
│
└── 📁 docs/                         # Documentação
    └── MVP_AGENTE_PESSOAL.md       # Documentação completa
```

---

## 🎯 Fluxo Recomendado de Leitura

### Para quem vai fazer deploy:

1. **Comece aqui:** `RESUMO_DEPLOY.md`
   - Entenda o processo geral

2. **Leia o guia completo:** `DEPLOY_COMPLETO.md`
   - Siga passo a passo

3. **Use os comandos:** `COMANDOS_DEPLOY.txt`
   - Copie e cole os comandos

4. **Configure n8n:** `workflows/N8N_WORKFLOW_GUIDE.md`
   - Após deploy funcionando

### Para quem vai configurar localmente:

1. **Setup inicial:** `SETUP.md`
2. **Configuração:** `CONFIGURAR.md`
3. **Próximos passos:** `PROXIMOS_PASSOS.md`

### Para entender o sistema:

1. **Visão geral:** `README.md`
2. **Documentação completa:** `docs/MVP_AGENTE_PESSOAL.md`
3. **Fluxo n8n:** `workflows/N8N_WORKFLOW_GUIDE.md`

---

## 🔍 Busca Rápida

### Quero fazer deploy:
→ `DEPLOY_COMPLETO.md` ou `COMANDOS_DEPLOY.txt`

### Quero configurar localmente:
→ `SETUP.md` ou `CONFIGURAR.md`

### Quero entender o sistema:
→ `docs/MVP_AGENTE_PESSOAL.md`

### Quero configurar n8n:
→ `workflows/N8N_WORKFLOW_GUIDE.md`

### Tenho um erro:
→ `DEPLOY_COMPLETO.md` (seção Troubleshooting)

### Quero testar conexão:
→ `scripts/test_connection.py`

### Quero criar banco:
→ `scripts/create_personal_agent_db.sql`

---

## ⚠️ Arquivos Importantes

### ⚠️ Editar ANTES de usar:
- `scripts/create_personal_agent_db.sql` - Alterar senha
- `.env` - Configurar credenciais
- `mcp_server/systemd/mcp-server.service` - Ajustar caminhos (se necessário)

### ✅ Prontos para usar:
- `scripts/deploy_servidor.sh` - Script automático
- `scripts/init_tables.py` - Inicializar tabelas
- `scripts/test_connection.py` - Testar conexão

---

## 📞 Suporte

Se tiver dúvidas:
1. Consulte a seção de Troubleshooting em `DEPLOY_COMPLETO.md`
2. Verifique os logs: `sudo journalctl -u mcp-server -f`
3. Teste a conexão: `python3 scripts/test_connection.py`
4. Verifique o status: `sudo systemctl status mcp-server`

---

**Boa sorte com o deploy! 🚀**
