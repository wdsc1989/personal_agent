"""
Serviço para gerar relatórios do agente pessoal
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Dict, Any, Optional
from datetime import date, datetime, timedelta
from decimal import Decimal
from collections import defaultdict

from models.personal_agent_mvp import ContaPagar
from services.personal_agent_service import PersonalAgentService


class ReportServicePersonal:
    """
    Serviço para gerar relatórios de contas a pagar pessoais
    """

    def __init__(self, db: Session):
        """
        Inicializa o serviço com uma sessão do banco de dados
        """
        self.db = db
        self.service = PersonalAgentService(db)

    def gerar_resumo_mensal(
        self,
        usuario_telegram_id: int,
        mes: Optional[int] = None,
        ano: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Gera resumo mensal das contas
        """
        hoje = date.today()
        if not mes:
            mes = hoje.month
        if not ano:
            ano = hoje.year

        # Primeiro e último dia do mês
        data_inicial = date(ano, mes, 1)
        if mes == 12:
            data_final = date(ano + 1, 1, 1) - timedelta(days=1)
        else:
            data_final = date(ano, mes + 1, 1) - timedelta(days=1)

        contas = self.service.listar_contas_por_periodo(
            usuario_telegram_id,
            data_inicial,
            data_final
        )

        total_pendente = Decimal('0')
        total_pago = Decimal('0')
        total_vencido = Decimal('0')
        total_cancelado = Decimal('0')
        contas_por_status = defaultdict(int)

        for conta in contas:
            valor = Decimal(str(conta.valor_total))
            contas_por_status[conta.status] += 1
            if conta.status == 'pendente':
                total_pendente += valor
            elif conta.status == 'pago':
                total_pago += valor
            elif conta.status == 'vencido':
                total_vencido += valor
            elif conta.status == 'cancelado':
                total_cancelado += valor

        return {
            'mes': mes,
            'ano': ano,
            'data_inicial': data_inicial.isoformat(),
            'data_final': data_final.isoformat(),
            'total_pendente': float(total_pendente),
            'total_pago': float(total_pago),
            'total_vencido': float(total_vencido),
            'total_cancelado': float(total_cancelado),
            'total_geral': float(total_pendente + total_pago + total_vencido + total_cancelado),
            'contas_por_status': dict(contas_por_status),
            'total_contas': len(contas)
        }

    def gerar_relatorio_por_categoria(
        self,
        usuario_telegram_id: int,
        data_inicial: Optional[date] = None,
        data_final: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Gera relatório agrupado por categoria
        """
        if not data_inicial:
            data_inicial = date.today().replace(day=1)
        if not data_final:
            hoje = date.today()
            if hoje.month == 12:
                data_final = date(hoje.year + 1, 1, 1) - timedelta(days=1)
            else:
                data_final = date(hoje.year, hoje.month + 1, 1) - timedelta(days=1)

        contas = self.service.listar_contas_por_periodo(
            usuario_telegram_id,
            data_inicial,
            data_final
        )

        por_categoria = defaultdict(lambda: {
            'total': Decimal('0'),
            'pendente': Decimal('0'),
            'pago': Decimal('0'),
            'vencido': Decimal('0'),
            'cancelado': Decimal('0'),
            'quantidade': 0
        })

        for conta in contas:
            categoria = conta.categoria or 'Sem categoria'
            valor = Decimal(str(conta.valor_total))

            por_categoria[categoria]['total'] += valor
            por_categoria[categoria]['quantidade'] += 1

            if conta.status == 'pendente':
                por_categoria[categoria]['pendente'] += valor
            elif conta.status == 'pago':
                por_categoria[categoria]['pago'] += valor
            elif conta.status == 'vencido':
                por_categoria[categoria]['vencido'] += valor
            elif conta.status == 'cancelado':
                por_categoria[categoria]['cancelado'] += valor

        # Converte Decimal para float
        resultado = {}
        for categoria, dados in por_categoria.items():
            resultado[categoria] = {
                'total': float(dados['total']),
                'pendente': float(dados['pendente']),
                'pago': float(dados['pago']),
                'vencido': float(dados['vencido']),
                'cancelado': float(dados['cancelado']),
                'quantidade': dados['quantidade']
            }

        return {
            'data_inicial': data_inicial.isoformat(),
            'data_final': data_final.isoformat(),
            'por_categoria': resultado
        }

    def gerar_relatorio_vencidas(
        self,
        usuario_telegram_id: int
    ) -> Dict[str, Any]:
        """
        Gera relatório de contas vencidas
        """
        contas_vencidas = self.service.buscar_vencidas(usuario_telegram_id)

        total_vencido = Decimal('0')
        contas_formatadas = []

        for conta in contas_vencidas:
            valor = Decimal(str(conta.valor_total))
            total_vencido += valor
            dias_vencido = (date.today() - conta.data_vencimento).days

            contas_formatadas.append({
                'id': conta.id,
                'nome_credor': conta.nome_credor,
                'valor_total': float(valor),
                'data_vencimento': conta.data_vencimento.isoformat(),
                'dias_vencido': dias_vencido,
                'categoria': conta.categoria,
                'descricao': conta.descricao
            })

        return {
            'total_vencido': float(total_vencido),
            'quantidade': len(contas_vencidas),
            'contas': contas_formatadas
        }

    def calcular_totais(
        self,
        usuario_telegram_id: int
    ) -> Dict[str, Any]:
        """
        Calcula totais gerais
        """
        return self.service.calcular_totais(usuario_telegram_id)

    def gerar_previsao_mensal(
        self,
        usuario_telegram_id: int,
        mes: Optional[int] = None,
        ano: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Gera previsão de gastos do mês
        """
        hoje = date.today()
        if not mes:
            mes = hoje.month
        if not ano:
            ano = hoje.year

        # Primeiro e último dia do mês
        data_inicial = date(ano, mes, 1)
        if mes == 12:
            data_final = date(ano + 1, 1, 1) - timedelta(days=1)
        else:
            data_final = date(ano, mes + 1, 1) - timedelta(days=1)

        contas = self.service.listar_contas_por_periodo(
            usuario_telegram_id,
            data_inicial,
            data_final
        )

        total_previsto = Decimal('0')
        total_pago = Decimal('0')
        total_pendente = Decimal('0')

        for conta in contas:
            valor = Decimal(str(conta.valor_total))
            total_previsto += valor

            if conta.status == 'pago':
                total_pago += valor
            elif conta.status in ['pendente', 'vencido']:
                total_pendente += valor

        return {
            'mes': mes,
            'ano': ano,
            'total_previsto': float(total_previsto),
            'total_pago': float(total_pago),
            'total_pendente': float(total_pendente),
            'quantidade_contas': len(contas)
        }

    def gerar_listagem_periodo(
        self,
        usuario_telegram_id: int,
        data_inicial: date,
        data_final: date,
        status: Optional[str] = None,
        categoria: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Gera listagem formatada de contas em um período
        """
        contas = self.service.listar_contas_por_periodo(
            usuario_telegram_id,
            data_inicial,
            data_final,
            status,
            categoria
        )

        listagem = []
        for conta in contas:
            listagem.append({
                'id': conta.id,
                'nome_credor': conta.nome_credor,
                'descricao': conta.descricao,
                'valor_total': float(conta.valor_total),
                'valor_pago': float(conta.valor_pago),
                'valor_restante': float(conta.valor_restante()),
                'data_vencimento': conta.data_vencimento.isoformat(),
                'data_pagamento': conta.data_pagamento.isoformat() if conta.data_pagamento else None,
                'status': conta.status,
                'categoria': conta.categoria,
                'numero_parcelas': conta.numero_parcelas,
                'parcela_atual': conta.parcela_atual,
                'esta_vencida': conta.esta_vencida(),
                'observacoes': conta.observacoes
            })

        return listagem
