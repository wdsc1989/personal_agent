"""
Serviço MCP para detecção de intenção
"""
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import re

from mcp_server.schemas.mcp import DetectResponse


class MCPDetector:
    """
    Detecta a intenção do usuário a partir do texto
    """

    def __init__(self, db: Session):
        self.db = db

    def detect(self, text: str, context: Optional[Dict[str, Any]] = None) -> DetectResponse:
        """
        Detecta a intenção do usuário
        """
        text_lower = text.lower().strip()

        # Padrões para detecção
        patterns = {
            'INSERT': [
                r'adicionar\s+conta',
                r'registrar\s+conta',
                r'criar\s+conta',
                r'novo\s+conta',
                r'inserir\s+conta',
                r'cadastrar\s+conta'
            ],
            'UPDATE': [
                r'atualizar\s+conta',
                r'editar\s+conta',
                r'alterar\s+conta',
                r'modificar\s+conta',
                r'atualizar',
                r'editar'
            ],
            'DELETE': [
                r'deletar\s+conta',
                r'excluir\s+conta',
                r'remover\s+conta',
                r'apagar\s+conta',
                r'deletar',
                r'excluir'
            ],
            'LIST': [
                r'mostrar\s+contas',
                r'listar\s+contas',
                r'ver\s+contas',
                r'minhas\s+contas',
                r'contas\s+de',
                r'contas\s+do',
                r'contas\s+entre',
                r'contas\s+pendentes',
                r'contas\s+vencidas',
                r'contas\s+pagas'
            ],
            'REPORT': [
                r'relat[oó]rio',
                r'resumo',
                r'total',
                r'estat[íi]stica',
                r'previs[ãa]o'
            ]
        }

        # Detecta ação
        action = 'OTHER'
        confidence = 0.0
        extracted_info = {}

        for action_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, text_lower):
                    action = action_type
                    confidence = 0.9
                    break
            if action != 'OTHER':
                break

        # Se não detectou, tenta inferir pelo contexto
        if action == 'OTHER' and context:
            if 'previous_action' in context:
                action = context['previous_action']
                confidence = 0.7

        # Extrai informações básicas
        if action in ['INSERT', 'UPDATE']:
            # Tenta extrair ID se for UPDATE
            id_match = re.search(r'id\s*[:=]?\s*(\d+)', text_lower)
            if id_match:
                extracted_info['id'] = int(id_match.group(1))

        return DetectResponse(
            action=action,
            entity='contas_pagar',
            confidence=confidence,
            extracted_info=extracted_info if extracted_info else None
        )
