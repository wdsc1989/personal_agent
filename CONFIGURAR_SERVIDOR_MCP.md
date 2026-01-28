# 🚀 Configurar Servidor MCP - Systemd

## Problema

O serviço `mcp-server.service` não foi encontrado. Precisamos configurá-lo.

---

## Solução Rápida

Execute no servidor:

```bash
cd /opt/personal_agent

# 1. Verificar se o arquivo de serviço existe
ls -la mcp_server/systemd/mcp-server.service

# 2. Copiar arquivo de serviço
sudo cp mcp_server/systemd/mcp-server.service /etc/systemd/system/

# 3. Editar arquivo de serviço (ajustar caminhos se necessário)
sudo nano /etc/systemd/system/mcp-server.service
```

**Verifique e ajuste no arquivo:**
- `WorkingDirectory=/opt/personal_agent/mcp_server`
- `ExecStart=/opt/personal_agent/venv/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8001`
- `Environment="PATH=/opt/personal_agent/venv/bin:/usr/bin:/usr/local/bin"`

**Salvar:** `Ctrl+O`, `Enter`, `Ctrl+X`

```bash
# 4. Recarregar systemd
sudo systemctl daemon-reload

# 5. Habilitar serviço (inicia automaticamente no boot)
sudo systemctl enable mcp-server

# 6. Iniciar serviço
sudo systemctl start mcp-server

# 7. Verificar status
sudo systemctl status mcp-server
```

---

## Passo a Passo Detalhado

### 1. Verificar Estrutura

```bash
cd /opt/personal_agent
ls -la mcp_server/
ls -la mcp_server/systemd/
```

### 2. Copiar Arquivo de Serviço

```bash
sudo cp mcp_server/systemd/mcp-server.service /etc/systemd/system/
```

### 3. Verificar/Editar Arquivo de Serviço

```bash
sudo nano /etc/systemd/system/mcp-server.service
```

**Conteúdo esperado:**

```ini
[Unit]
Description=MCP Server - Agente Pessoal
After=network.target postgresql.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/personal_agent/mcp_server
Environment="PATH=/opt/personal_agent/venv/bin:/usr/bin:/usr/local/bin"
ExecStart=/opt/personal_agent/venv/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Ajuste os caminhos se necessário:**
- Se o venv estiver em outro lugar, ajuste `ExecStart` e `Environment`
- Se não usar venv, use: `ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8001`

**Salvar:** `Ctrl+O`, `Enter`, `Ctrl+X`

### 4. Configurar e Iniciar

```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar serviço
sudo systemctl enable mcp-server

# Iniciar serviço
sudo systemctl start mcp-server

# Verificar status
sudo systemctl status mcp-server
```

### 5. Testar Servidor

```bash
# Testar endpoint de health
curl http://localhost:8001/health

# Ou testar endpoint raiz
curl http://localhost:8001/

# Testar endpoint de detecção
curl -X POST http://localhost:8001/mcp/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "adicionar conta teste", "context": {}}'
```

---

## Verificar Logs

```bash
# Ver logs em tempo real
sudo journalctl -u mcp-server -f

# Ver últimas 50 linhas
sudo journalctl -u mcp-server -n 50

# Ver logs desde hoje
sudo journalctl -u mcp-server --since today
```

---

## Troubleshooting

### Serviço não inicia

1. **Verificar logs:**
   ```bash
   sudo journalctl -u mcp-server -n 100
   ```

2. **Testar manualmente:**
   ```bash
   cd /opt/personal_agent
   source venv/bin/activate
   cd mcp_server
   python3 main.py
   ```

3. **Verificar se porta está livre:**
   ```bash
   sudo netstat -tlnp | grep 8001
   # ou
   sudo ss -tlnp | grep 8001
   ```

### Erro de importação

Se der erro de importação, verifique se o venv está ativado e as dependências instaladas:

```bash
cd /opt/personal_agent
source venv/bin/activate
pip list | grep fastapi
pip list | grep uvicorn
```

### Erro de conexão com banco

Verifique o arquivo `.env`:

```bash
cat /opt/personal_agent/.env
```

---

## Comandos Úteis

```bash
# Parar serviço
sudo systemctl stop mcp-server

# Reiniciar serviço
sudo systemctl restart mcp-server

# Ver status
sudo systemctl status mcp-server

# Desabilitar serviço (não inicia no boot)
sudo systemctl disable mcp-server

# Ver logs
sudo journalctl -u mcp-server -f
```

---

## Verificação Final

Após configurar, verifique:

- [ ] Serviço está rodando: `sudo systemctl status mcp-server`
- [ ] Endpoint responde: `curl http://localhost:8001/health`
- [ ] Logs sem erros: `sudo journalctl -u mcp-server -n 20`

---

**Após configurar, o servidor MCP estará disponível em `http://localhost:8001` 🚀**
