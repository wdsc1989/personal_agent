"""
Modelos do Agente Pessoal MVP
Todas as colunas estão em português conforme especificado no plano
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Numeric, Text, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime, date
from config.database import BasePersonal


class UsuarioTelegram(BasePersonal):
    """
    Modelo de usuário do Telegram
    Mapeia a tabela usuarios_telegram
    """
    __tablename__ = 'usuarios_telegram'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    nome_usuario = Column(String(100), nullable=True)
    primeiro_nome = Column(String(100), nullable=False)
    ultimo_nome = Column(String(100), nullable=True)
    telefone = Column(String(20), nullable=True)
    codigo_idioma = Column(String(10), default='pt-BR', nullable=False)
    preferencias = Column(Text, nullable=True)  # JSON armazenado como texto
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    ultimo_acesso = Column(DateTime, nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)

    # Relacionamentos
    contas_pagar = relationship('ContaPagar', back_populates='usuario_telegram', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<UsuarioTelegram(telegram_id={self.telegram_id}, primeiro_nome='{self.primeiro_nome}')>"

    def atualizar_ultimo_acesso(self):
        """Atualiza o timestamp do último acesso"""
        self.ultimo_acesso = datetime.utcnow()


class ContaPagar(BasePersonal):
    """
    Modelo de conta a pagar pessoal
    Mapeia a tabela contas_pagar
    """
    __tablename__ = 'contas_pagar'

    id = Column(Integer, primary_key=True, index=True)
    usuario_telegram_id = Column(Integer, ForeignKey('usuarios_telegram.id', ondelete='CASCADE'), nullable=False)
    nome_credor = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=True)
    valor_total = Column(Numeric(10, 2), nullable=False)
    valor_pago = Column(Numeric(10, 2), default=0, nullable=False)
    data_vencimento = Column(Date, nullable=False)
    data_pagamento = Column(Date, nullable=True)
    numero_parcelas = Column(Integer, nullable=True)
    parcela_atual = Column(Integer, nullable=True)
    status = Column(String(20), default='pendente', nullable=False)
    categoria = Column(String(50), nullable=True)
    observacoes = Column(Text, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, nullable=True)

    # Relacionamentos
    usuario_telegram = relationship('UsuarioTelegram', back_populates='contas_pagar')

    def __repr__(self):
        return f"<ContaPagar(id={self.id}, nome_credor='{self.nome_credor}', valor_total={self.valor_total})>"

    def valor_restante(self):
        """Calcula o valor restante a pagar"""
        return float(self.valor_total) - float(self.valor_pago)

    def esta_vencida(self):
        """Verifica se a conta está vencida"""
        if self.status == 'pago' or self.status == 'cancelado':
            return False
        return date.today() > self.data_vencimento

    def marcar_como_pago(self, data_pagamento=None):
        """Marca a conta como paga"""
        self.status = 'pago'
        self.valor_pago = self.valor_total
        if data_pagamento:
            self.data_pagamento = data_pagamento
        else:
            self.data_pagamento = date.today()
        self.atualizado_em = datetime.utcnow()

    def atualizar_status_vencido(self):
        """Atualiza o status para vencido se a data de vencimento passou"""
        if self.status == 'pendente' and self.esta_vencida():
            self.status = 'vencido'
            self.atualizado_em = datetime.utcnow()
