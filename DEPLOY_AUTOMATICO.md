# 🚀 Deploy Automático - Agente Pessoal

Este guia mostra como fazer o deploy **totalmente automático** no servidor.

---

## 📋 Pré-requisitos

1. ✅ Repositório Git configurado: `https://github.com/wdsc1989/personal_agent.git`
2. ✅ Acesso SSH ao servidor: `srv1140258.hstgr.cloud`
3. ✅ Chave SSH configurada no servidor para acessar o GitHub

---

## 🎯 Processo em 2 Passos

### PASSO 1: Preparar e Enviar para Git (Local)

**No seu computador Windows:**

```bash
cd c:\Users\DELL\Documents\Projetos\Contabil\personal_agent
scripts\preparar_deploy_local.bat
```

**OU manualmente:**

```bash
git add .
git commit -m "Deploy: Preparacao para servidor"
git push origin main
```

---

### PASSO 2: Deploy Automático no Servidor

**Conecte-se ao servidor:**

```bash
ssh root@srv1140258.hstgr.cloud
```

**Execute o script de deploy:**

```bash
cd /opt
git clone https://github.com/wdsc1989/personal_agent.git
cd personal_agent
bash scripts/deploy_completo.sh
```

O script fará **TUDO automaticamente**:
- ✅ Clonar/atualizar repositório
- ✅ Criar ambiente virtual
- ✅ Instalar dependências
- ✅ Configurar .env (solicitará senha do banco)
- ✅ Criar banco de dados
- ✅ Criar tabelas
- ✅ Configurar serviço systemd
- ✅ Iniciar servidor MCP
- ✅ Verificar se está funcionando

---

## 🔧 O que o Script Faz

O script `deploy_completo.sh` executa automaticamente:

1. **Preparação**
   - Cria/atualiza diretório `/opt/personal_agent`
   - Clona ou atualiza repositório Git

2. **Ambiente Python**
   - Cria ambiente virtual
   - Instala todas as dependências

3. **Configuração**
   - Cria arquivo `.env` (solicita senha do banco)
   - Configura conexão com PostgreSQL

4. **Banco de Dados**
   - Cria banco `personal_agent_db`
   - Cria usuário `personal_agent_user`
   - Cria todas as tabelas

5. **Servidor MCP**
   - Configura serviço systemd
   - Inicia servidor na porta 8001

6. **Verificação**
   - Testa conexão com banco
   - Verifica se servidor está rodando
   - Testa endpoint de health

---

## ⚙️ Durante a Execução

O script irá solicitar:

1. **Senha do banco de dados** (quando criar .env)
   - Digite a senha que será usada para o usuário `personal_agent_user`
   - A senha será salva no arquivo `.env`

2. **Confirmações** (se algo já existir)
   - Se o diretório já existir: confirmação para continuar
   - Se o banco já existir: opção de recriar ou manter

---

## ✅ Verificação Pós-Deploy

Após o script terminar, verifique:

```bash
# Status do serviço
sudo systemctl status mcp-server

# Logs
sudo journalctl -u mcp-server -f

# Testar servidor
curl http://localhost:8001/health
```

---

## 🔄 Atualizações Futuras

Para atualizar o sistema no servidor:

```bash
ssh root@srv1140258.hstgr.cloud
cd /opt/personal_agent
git pull
bash scripts/deploy_completo.sh
```

O script detectará o que já existe e atualizará apenas o necessário.

---

## 🆘 Troubleshooting

### Erro ao clonar repositório

```bash
# Verificar chave SSH
ssh -T git@github.com

# Se não funcionar, configure a chave SSH no servidor
```

### Erro ao criar banco

```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Verificar se usuário postgres tem acesso
sudo -u postgres psql
```

### Serviço não inicia

```bash
# Ver logs detalhados
sudo journalctl -u mcp-server -n 100

# Testar manualmente
cd /opt/personal_agent
source venv/bin/activate
cd mcp_server
python3 main.py
```

---

## 📝 Notas Importantes

1. **Senha do Banco**: Escolha uma senha forte e segura
2. **Primeira Execução**: O script criará tudo do zero
3. **Atualizações**: O script é inteligente e não recria o que já existe
4. **Backup**: Antes de recriar banco, faça backup se houver dados importantes

---

## 🎉 Pronto!

Após o deploy automático, o sistema estará rodando em:
- **Servidor MCP**: `http://localhost:8001`
- **Banco de Dados**: `personal_agent_db`

**Próximo passo**: Configure o fluxo n8n seguindo `workflows/N8N_WORKFLOW_GUIDE.md`

---

**Deploy totalmente automático! 🚀**
