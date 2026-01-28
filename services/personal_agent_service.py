"""
Serviço para gerenciar operações CRUD do agente pessoal
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta
from decimal import Decimal

from models.personal_agent_mvp import UsuarioTelegram, ContaPagar
from config.database import SessionLocalPersonal


class PersonalAgentService:
    """
    Serviço para operações CRUD de contas a pagar pessoais
    """

    def __init__(self, db: Session):
        """
        Inicializa o serviço com uma sessão do banco de dados
        """
        self.db = db

    # ==================== USUÁRIOS TELEGRAM ====================

    def criar_ou_buscar_usuario_telegram(
        self,
        telegram_id: int,
        primeiro_nome: str,
        nome_usuario: Optional[str] = None,
        ultimo_nome: Optional[str] = None,
        telefone: Optional[str] = None,
        codigo_idioma: str = 'pt-BR'
    ) -> UsuarioTelegram:
        """
        Cria um novo usuário do Telegram ou retorna o existente
        """
        usuario = self.db.query(UsuarioTelegram).filter(
            UsuarioTelegram.telegram_id == telegram_id
        ).first()

        if usuario:
            # Atualiza informações se necessário
            usuario.primeiro_nome = primeiro_nome
            if nome_usuario:
                usuario.nome_usuario = nome_usuario
            if ultimo_nome:
                usuario.ultimo_nome = ultimo_nome
            if telefone:
                usuario.telefone = telefone
            usuario.ultimo_acesso = datetime.utcnow()
            usuario.ativo = True
            self.db.commit()
            self.db.refresh(usuario)
            return usuario

        # Cria novo usuário
        usuario = UsuarioTelegram(
            telegram_id=telegram_id,
            nome_usuario=nome_usuario,
            primeiro_nome=primeiro_nome,
            ultimo_nome=ultimo_nome,
            telefone=telefone,
            codigo_idioma=codigo_idioma,
            ultimo_acesso=datetime.utcnow()
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def buscar_usuario_por_telegram_id(self, telegram_id: int) -> Optional[UsuarioTelegram]:
        """
        Busca usuário por telegram_id
        """
        return self.db.query(UsuarioTelegram).filter(
            UsuarioTelegram.telegram_id == telegram_id
        ).first()

    # ==================== CONTAS A PAGAR ====================

    def criar_conta_pagar(
        self,
        usuario_telegram_id: int,
        nome_credor: str,
        valor_total: float,
        data_vencimento: date,
        descricao: Optional[str] = None,
        categoria: Optional[str] = None,
        numero_parcelas: Optional[int] = None,
        parcela_atual: Optional[int] = None,
        observacoes: Optional[str] = None
    ) -> ContaPagar:
        """
        Cria uma nova conta a pagar
        """
        conta = ContaPagar(
            usuario_telegram_id=usuario_telegram_id,
            nome_credor=nome_credor,
            descricao=descricao,
            valor_total=Decimal(str(valor_total)),
            valor_pago=Decimal('0'),
            data_vencimento=data_vencimento,
            numero_parcelas=numero_parcelas,
            parcela_atual=parcela_atual,
            status='pendente',
            categoria=categoria,
            observacoes=observacoes
        )
        self.db.add(conta)
        self.db.commit()
        self.db.refresh(conta)
        return conta

    def listar_contas_pagar(
        self,
        usuario_telegram_id: int,
        status: Optional[str] = None,
        categoria: Optional[str] = None
    ) -> List[ContaPagar]:
        """
        Lista todas as contas a pagar do usuário
        """
        query = self.db.query(ContaPagar).filter(
            ContaPagar.usuario_telegram_id == usuario_telegram_id
        )

        if status:
            query = query.filter(ContaPagar.status == status)

        if categoria:
            query = query.filter(ContaPagar.categoria == categoria)

        return query.order_by(ContaPagar.data_vencimento).all()

    def listar_contas_por_periodo(
        self,
        usuario_telegram_id: int,
        data_inicial: date,
        data_final: date,
        status: Optional[str] = None,
        categoria: Optional[str] = None
    ) -> List[ContaPagar]:
        """
        Lista contas a pagar dentro de um período
        """
        query = self.db.query(ContaPagar).filter(
            and_(
                ContaPagar.usuario_telegram_id == usuario_telegram_id,
                ContaPagar.data_vencimento >= data_inicial,
                ContaPagar.data_vencimento <= data_final
            )
        )

        if status:
            query = query.filter(ContaPagar.status == status)

        if categoria:
            query = query.filter(ContaPagar.categoria == categoria)

        return query.order_by(ContaPagar.data_vencimento).all()

    def buscar_conta_por_id(
        self,
        conta_id: int,
        usuario_telegram_id: int
    ) -> Optional[ContaPagar]:
        """
        Busca uma conta por ID (verificando se pertence ao usuário)
        """
        return self.db.query(ContaPagar).filter(
            and_(
                ContaPagar.id == conta_id,
                ContaPagar.usuario_telegram_id == usuario_telegram_id
            )
        ).first()

    def buscar_por_status(
        self,
        usuario_telegram_id: int,
        status: str
    ) -> List[ContaPagar]:
        """
        Busca contas por status
        """
        return self.db.query(ContaPagar).filter(
            and_(
                ContaPagar.usuario_telegram_id == usuario_telegram_id,
                ContaPagar.status == status
            )
        ).order_by(ContaPagar.data_vencimento).all()

    def buscar_vencidas(
        self,
        usuario_telegram_id: int
    ) -> List[ContaPagar]:
        """
        Busca contas vencidas (pendentes com data de vencimento passada)
        """
        hoje = date.today()
        contas = self.db.query(ContaPagar).filter(
            and_(
                ContaPagar.usuario_telegram_id == usuario_telegram_id,
                ContaPagar.status.in_(['pendente', 'vencido']),
                ContaPagar.data_vencimento < hoje
            )
        ).order_by(ContaPagar.data_vencimento).all()

        # Atualiza status para vencido se necessário
        for conta in contas:
            if conta.status == 'pendente':
                conta.status = 'vencido'
                conta.atualizado_em = datetime.utcnow()

        self.db.commit()
        return contas

    def atualizar_conta_pagar(
        self,
        conta_id: int,
        usuario_telegram_id: int,
        **kwargs
    ) -> Optional[ContaPagar]:
        """
        Atualiza uma conta a pagar
        """
        conta = self.buscar_conta_por_id(conta_id, usuario_telegram_id)
        if not conta:
            return None

        # Campos permitidos para atualização
        campos_permitidos = [
            'nome_credor', 'descricao', 'valor_total', 'valor_pago',
            'data_vencimento', 'data_pagamento', 'numero_parcelas',
            'parcela_atual', 'status', 'categoria', 'observacoes'
        ]

        for campo, valor in kwargs.items():
            if campo in campos_permitidos:
                if campo in ['valor_total', 'valor_pago']:
                    setattr(conta, campo, Decimal(str(valor)))
                else:
                    setattr(conta, campo, valor)

        conta.atualizado_em = datetime.utcnow()
        self.db.commit()
        self.db.refresh(conta)
        return conta

    def marcar_como_pago(
        self,
        conta_id: int,
        usuario_telegram_id: int,
        data_pagamento: Optional[date] = None
    ) -> Optional[ContaPagar]:
        """
        Marca uma conta como paga
        """
        conta = self.buscar_conta_por_id(conta_id, usuario_telegram_id)
        if not conta:
            return None

        conta.marcar_como_pago(data_pagamento)
        self.db.commit()
        self.db.refresh(conta)
        return conta

    def deletar_conta_pagar(
        self,
        conta_id: int,
        usuario_telegram_id: int
    ) -> bool:
        """
        Deleta uma conta a pagar
        """
        conta = self.buscar_conta_por_id(conta_id, usuario_telegram_id)
        if not conta:
            return False

        self.db.delete(conta)
        self.db.commit()
        return True

    def calcular_totais(
        self,
        usuario_telegram_id: int
    ) -> Dict[str, Any]:
        """
        Calcula totais de contas do usuário
        """
        contas = self.listar_contas_pagar(usuario_telegram_id)

        total_pendente = Decimal('0')
        total_pago = Decimal('0')
        total_vencido = Decimal('0')
        total_cancelado = Decimal('0')

        for conta in contas:
            valor = Decimal(str(conta.valor_total))
            if conta.status == 'pendente':
                total_pendente += valor
            elif conta.status == 'pago':
                total_pago += valor
            elif conta.status == 'vencido':
                total_vencido += valor
            elif conta.status == 'cancelado':
                total_cancelado += valor

        return {
            'total_pendente': float(total_pendente),
            'total_pago': float(total_pago),
            'total_vencido': float(total_vencido),
            'total_cancelado': float(total_cancelado),
            'total_geral': float(total_pendente + total_pago + total_vencido + total_cancelado)
        }
