"""
Serviço MCP para extração de dados
"""
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from datetime import date, datetime
import re
from decimal import Decimal

from mcp_server.schemas.mcp import ExtractResponse


class MCPExtractor:
    """
    Extrai dados estruturados do texto
    """

    def __init__(self, db: Session):
        self.db = db

    def extract(self, text: str, action: str, context: Optional[Dict[str, Any]] = None) -> ExtractResponse:
        """
        Extrai dados do texto baseado na ação
        """
        text_lower = text.lower()
        data = {}
        missing_fields = []
        confidence = 0.0

        if action == 'INSERT':
            data, missing_fields, confidence = self._extract_insert_data(text, text_lower)
        elif action == 'UPDATE':
            data, missing_fields, confidence = self._extract_update_data(text, text_lower)
        elif action == 'DELETE':
            data, missing_fields, confidence = self._extract_delete_data(text, text_lower)
        elif action == 'LIST':
            data, missing_fields, confidence = self._extract_list_filters(text, text_lower)

        return ExtractResponse(
            data=data,
            confidence=confidence,
            missing_fields=missing_fields
        )

    def _extract_insert_data(self, text: str, text_lower: str) -> tuple:
        """Extrai dados para INSERT"""
        data = {}
        missing_fields = []
        confidence = 0.0
        found_fields = 0

        # Nome do credor
        credor_patterns = [
            r'credor[:\s]+([^,\.]+)',
            r'fornecedor[:\s]+([^,\.]+)',
            r'para\s+([^,\.]+)',
            r'de\s+([^,\.]+)'
        ]
        for pattern in credor_patterns:
            match = re.search(pattern, text_lower)
            if match:
                data['nome_credor'] = match.group(1).strip().title()
                found_fields += 1
                break

        if 'nome_credor' not in data:
            missing_fields.append('nome_credor')

        # Valor
        valor_patterns = [
            r'valor[:\s]+r\$\s*([\d,\.]+)',
            r'r\$\s*([\d,\.]+)',
            r'([\d,\.]+)\s*reais',
            r'([\d,\.]+)\s*r\$'
        ]
        for pattern in valor_patterns:
            match = re.search(pattern, text_lower)
            if match:
                valor_str = match.group(1).replace(',', '.')
                try:
                    data['valor_total'] = float(valor_str)
                    found_fields += 1
                except:
                    pass
                break

        if 'valor_total' not in data:
            missing_fields.append('valor_total')

        # Data de vencimento
        data_patterns = [
            r'vencimento[:\s]+(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2,4})',
            r'data[:\s]+(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2,4})',
            r'(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2,4})',
            r'(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})'
        ]
        for pattern in data_patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    if len(match.groups()) == 3:
                        dia, mes, ano = match.groups()
                        if len(ano) == 2:
                            ano = '20' + ano
                        data['data_vencimento'] = date(int(ano), int(mes), int(dia)).isoformat()
                        found_fields += 1
                        break
                except:
                    pass

        if 'data_vencimento' not in data:
            missing_fields.append('data_vencimento')

        # Categoria (opcional)
        categoria_patterns = [
            r'categoria[:\s]+([^,\.]+)',
            r'tipo[:\s]+([^,\.]+)'
        ]
        for pattern in categoria_patterns:
            match = re.search(pattern, text_lower)
            if match:
                data['categoria'] = match.group(1).strip()
                break

        # Descrição (opcional)
        desc_patterns = [
            r'descri[çc][ãa]o[:\s]+([^\.]+)',
            r'obs[:\s]+([^\.]+)'
        ]
        for pattern in desc_patterns:
            match = re.search(pattern, text_lower)
            if match:
                data['descricao'] = match.group(1).strip()
                break

        # Calcula confiança
        total_required = 3  # nome_credor, valor_total, data_vencimento
        confidence = found_fields / total_required if total_required > 0 else 0.0

        return data, missing_fields, confidence

    def _extract_update_data(self, text: str, text_lower: str) -> tuple:
        """Extrai dados para UPDATE"""
        data = {}
        missing_fields = []
        confidence = 0.0

        # ID da conta
        id_match = re.search(r'id\s*[:=]?\s*(\d+)', text_lower)
        if id_match:
            data['id'] = int(id_match.group(1))
            confidence = 0.5
        else:
            missing_fields.append('id')

        # Campos a atualizar (similar ao INSERT)
        insert_data, _, _ = self._extract_insert_data(text, text_lower)
        data.update(insert_data)

        return data, missing_fields, confidence

    def _extract_delete_data(self, text: str, text_lower: str) -> tuple:
        """Extrai dados para DELETE"""
        data = {}
        missing_fields = []
        confidence = 0.0

        # ID da conta
        id_match = re.search(r'id\s*[:=]?\s*(\d+)', text_lower)
        if id_match:
            data['id'] = int(id_match.group(1))
            confidence = 0.9
        else:
            missing_fields.append('id')

        return data, missing_fields, confidence

    def _extract_list_filters(self, text: str, text_lower: str) -> tuple:
        """Extrai filtros para LIST"""
        data = {}
        missing_fields = []
        confidence = 0.5

        # Período
        # Tenta extrair datas
        data_patterns = [
            r'de\s+(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2,4})\s+at[ée]\s+(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2,4})',
            r'entre\s+(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2,4})\s+e\s+(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2,4})'
        ]
        for pattern in data_patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    dia1, mes1, ano1, dia2, mes2, ano2 = match.groups()
                    if len(ano1) == 2:
                        ano1 = '20' + ano1
                    if len(ano2) == 2:
                        ano2 = '20' + ano2
                    data['data_inicial'] = date(int(ano1), int(mes1), int(dia1)).isoformat()
                    data['data_final'] = date(int(ano2), int(mes2), int(dia2)).isoformat()
                    confidence = 0.8
                    break
                except:
                    pass

        # Status
        if 'pendente' in text_lower:
            data['status'] = 'pendente'
        elif 'pago' in text_lower or 'pagas' in text_lower:
            data['status'] = 'pago'
        elif 'vencido' in text_lower or 'vencidas' in text_lower:
            data['status'] = 'vencido'

        # Categoria
        categoria_match = re.search(r'categoria[:\s]+([^,\.]+)', text_lower)
        if categoria_match:
            data['categoria'] = categoria_match.group(1).strip()

        return data, missing_fields, confidence
