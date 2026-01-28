# ✅ Próximos Passos Após Conexão Estabelecida

## Status Atual

✅ Conexão com banco de dados estabelecida com sucesso!

---

## Próximos Passos

### 1. Inicializar Tabelas

Se as tabelas ainda não foram criadas:

```bash
cd /opt/personal_agent
source venv/bin/activate
python3 scripts/init_tables.py
```

Isso criará as tabelas:
- `usuarios_telegram`
- `contas_pagar`

### 2. Verificar se Tabelas Existem

```bash
sudo -u postgres psql -d personal_agent_db -c "\dt"
```

Deve mostrar as tabelas criadas.

### 3. Iniciar Servidor MCP

```bash
cd /opt/personal_agent

# Verificar se o serviço está configurado
sudo systemctl status mcp-server

# Se não estiver rodando, iniciar
sudo systemctl start mcp-server

# Verificar status
sudo systemctl status mcp-server
```

### 4. Testar Servidor MCP

```bash
# Testar endpoint de health
curl http://localhost:8001/health

# Ou testar endpoint de detecção
curl -X POST http://localhost:8001/mcp/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "adicionar conta teste", "context": {}}'
```

### 5. Verificar Logs do Servidor MCP

```bash
sudo journalctl -u mcp-server -f
```

---

## Checklist Completo

- [x] ✅ Conexão com banco estabelecida
- [ ] Inicializar tabelas
- [ ] Verificar tabelas criadas
- [ ] Iniciar servidor MCP
- [ ] Testar servidor MCP
- [ ] Configurar fluxo n8n

---

## Se o Servidor MCP Não Estiver Configurado

Execute o script de deploy completo:

```bash
cd /opt/personal_agent
bash scripts/deploy_completo.sh
```

Ou configure manualmente:

```bash
# Copiar arquivo de serviço
sudo cp mcp_server/systemd/mcp-server.service /etc/systemd/system/

# Ajustar caminhos no arquivo (se necessário)
sudo nano /etc/systemd/system/mcp-server.service

# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar serviço
sudo systemctl enable mcp-server

# Iniciar serviço
sudo systemctl start mcp-server

# Verificar status
sudo systemctl status mcp-server
```

---

## Próximo Passo: Configurar n8n

Após tudo funcionando, configure o fluxo n8n seguindo:
- `workflows/N8N_WORKFLOW_GUIDE.md`

**URL do servidor MCP no n8n:**
- `http://localhost:8001` (se n8n estiver no mesmo servidor)

---

**Tudo pronto para continuar! 🚀**
