-- ============================================
-- CRIAR BANCO DE DADOS PERSONAL_AGENT_DB
-- ============================================

-- 1. Criar banco de dados
CREATE DATABASE personal_agent_db;

-- 2. Criar usuário
CREATE USER personal_agent_user WITH PASSWORD 'SENHA_SEGURA_AQUI';

-- 3. Dar permissões
GRANT ALL PRIVILEGES ON DATABASE personal_agent_db TO personal_agent_user;

-- 4. Conectar ao banco
\c personal_agent_db

-- 5. Dar permissões no schema
GRANT ALL ON SCHEMA public TO personal_agent_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO personal_agent_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO personal_agent_user;

-- ============================================
-- TABELA: usuarios_telegram
-- ============================================
CREATE TABLE usuarios_telegram (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    nome_usuario VARCHAR(100),
    primeiro_nome VARCHAR(100) NOT NULL,
    ultimo_nome VARCHAR(100),
    telefone VARCHAR(20),
    codigo_idioma VARCHAR(10) DEFAULT 'pt-BR',
    preferencias JSONB,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_acesso TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_usuarios_telegram_id ON usuarios_telegram(telegram_id);
CREATE INDEX idx_usuarios_telegram_ativo ON usuarios_telegram(ativo);

-- ============================================
-- TABELA: contas_pagar
-- ============================================
CREATE TABLE contas_pagar (
    id SERIAL PRIMARY KEY,
    usuario_telegram_id INTEGER NOT NULL REFERENCES usuarios_telegram(id) ON DELETE CASCADE,
    nome_credor VARCHAR(200) NOT NULL,
    descricao TEXT,
    valor_total DECIMAL(10,2) NOT NULL CHECK (valor_total > 0),
    valor_pago DECIMAL(10,2) DEFAULT 0 CHECK (valor_pago >= 0),
    data_vencimento DATE NOT NULL,
    data_pagamento DATE,
    numero_parcelas INTEGER CHECK (numero_parcelas > 0),
    parcela_atual INTEGER CHECK (parcela_atual > 0),
    status VARCHAR(20) DEFAULT 'pendente' CHECK (status IN ('pendente', 'pago', 'cancelado', 'vencido')),
    categoria VARCHAR(50),
    observacoes TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP
);

CREATE INDEX idx_contas_pagar_usuario ON contas_pagar(usuario_telegram_id);
CREATE INDEX idx_contas_pagar_vencimento ON contas_pagar(data_vencimento);
CREATE INDEX idx_contas_pagar_status ON contas_pagar(status);
CREATE INDEX idx_contas_pagar_usuario_status ON contas_pagar(usuario_telegram_id, status);

-- ============================================
-- TRIGGER: Atualizar atualizado_em automaticamente
-- ============================================
CREATE OR REPLACE FUNCTION atualizar_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizado_em = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_atualizar_contas_pagar
    BEFORE UPDATE ON contas_pagar
    FOR EACH ROW
    EXECUTE FUNCTION atualizar_timestamp();

-- ============================================
-- PERMISSÕES FINAIS
-- ============================================
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO personal_agent_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO personal_agent_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO personal_agent_user;
