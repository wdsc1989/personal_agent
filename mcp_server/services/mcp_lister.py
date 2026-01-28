"""
Serviço MCP para listagem de contas
"""
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from datetime import date

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from services.personal_agent_service import PersonalAgentService
from mcp_server.schemas.mcp import ListResponse


class MCPLister:
    """
    Lista contas com filtros
    """

    def __init__(self, db: Session):
        self.db = db
        self.service = PersonalAgentService(db)

    def list_accounts(
        self,
        usuario_telegram_id: int,
        data_inicial: Optional[date] = None,
        data_final: Optional[date] = None,
        status: Optional[str] = None,
        categoria: Optional[str] = None
    ) -> ListResponse:
        """
        Lista contas com filtros aplicados
        """
        # Se tem período, usa listar_contas_por_periodo
        if data_inicial and data_final:
            contas = self.service.listar_contas_por_periodo(
                usuario_telegram_id,
                data_inicial,
                data_final,
                status,
                categoria
            )
        else:
            # Senão, usa listar_contas_pagar
            contas = self.service.listar_contas_pagar(
                usuario_telegram_id,
                status,
                categoria
            )

        # Formata contas
        contas_formatadas = []
        total_valor = 0.0

        for conta in contas:
            contas_formatadas.append({
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
            total_valor += float(conta.valor_total)

        return ListResponse(
            contas=contas_formatadas,
            total=len(contas_formatadas),
            total_valor=total_valor
        )
