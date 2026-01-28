"""
Serviço MCP para validação de dados
"""
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from datetime import date, datetime
from decimal import Decimal

from mcp_server.schemas.mcp import ValidateResponse


class MCPValidator:
    """
    Valida dados antes de salvar
    """

    def __init__(self, db: Session):
        self.db = db

    def validate(self, data: Dict[str, Any], action: str) -> ValidateResponse:
        """
        Valida dados baseado na ação
        """
        errors = []
        warnings = []

        if action == 'INSERT':
            errors, warnings = self._validate_insert(data)
        elif action == 'UPDATE':
            errors, warnings = self._validate_update(data)
        elif action == 'DELETE':
            errors, warnings = self._validate_delete(data)

        return ValidateResponse(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def _validate_insert(self, data: Dict[str, Any]) -> tuple:
        """Valida dados para INSERT"""
        errors = []
        warnings = []

        # Campos obrigatórios
        required_fields = ['nome_credor', 'valor_total', 'data_vencimento']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Campo obrigatório faltando: {field}")

        # Valida nome_credor
        if 'nome_credor' in data:
            if not isinstance(data['nome_credor'], str) or len(data['nome_credor'].strip()) == 0:
                errors.append("nome_credor deve ser uma string não vazia")
            elif len(data['nome_credor']) > 200:
                errors.append("nome_credor deve ter no máximo 200 caracteres")

        # Valida valor_total
        if 'valor_total' in data:
            try:
                valor = float(data['valor_total'])
                if valor <= 0:
                    errors.append("valor_total deve ser maior que zero")
            except (ValueError, TypeError):
                errors.append("valor_total deve ser um número válido")

        # Valida data_vencimento
        if 'data_vencimento' in data:
            try:
                if isinstance(data['data_vencimento'], str):
                    data_obj = date.fromisoformat(data['data_vencimento'])
                else:
                    data_obj = data['data_vencimento']
                
                if data_obj < date.today():
                    warnings.append("data_vencimento está no passado")
            except (ValueError, TypeError):
                errors.append("data_vencimento deve ser uma data válida (formato: YYYY-MM-DD)")

        # Valida categoria (opcional)
        if 'categoria' in data and data['categoria']:
            if len(data['categoria']) > 50:
                errors.append("categoria deve ter no máximo 50 caracteres")

        # Valida numero_parcelas (opcional)
        if 'numero_parcelas' in data and data['numero_parcelas']:
            try:
                parcelas = int(data['numero_parcelas'])
                if parcelas <= 0:
                    errors.append("numero_parcelas deve ser maior que zero")
            except (ValueError, TypeError):
                errors.append("numero_parcelas deve ser um número inteiro válido")

        # Valida parcela_atual (opcional)
        if 'parcela_atual' in data and data['parcela_atual']:
            try:
                parcela = int(data['parcela_atual'])
                if parcela <= 0:
                    errors.append("parcela_atual deve ser maior que zero")
                
                # Se tem numero_parcelas, valida se parcela_atual <= numero_parcelas
                if 'numero_parcelas' in data and data['numero_parcelas']:
                    if parcela > int(data['numero_parcelas']):
                        errors.append("parcela_atual não pode ser maior que numero_parcelas")
            except (ValueError, TypeError):
                errors.append("parcela_atual deve ser um número inteiro válido")

        return errors, warnings

    def _validate_update(self, data: Dict[str, Any]) -> tuple:
        """Valida dados para UPDATE"""
        errors = []
        warnings = []

        # ID é obrigatório
        if 'id' not in data or not data['id']:
            errors.append("Campo obrigatório faltando: id")

        # Valida ID
        if 'id' in data:
            try:
                conta_id = int(data['id'])
                if conta_id <= 0:
                    errors.append("id deve ser um número inteiro positivo")
            except (ValueError, TypeError):
                errors.append("id deve ser um número inteiro válido")

        # Valida campos opcionais (mesma validação do INSERT)
        insert_errors, insert_warnings = self._validate_insert(data)
        errors.extend([e for e in insert_errors if 'obrigatório' not in e])
        warnings.extend(insert_warnings)

        return errors, warnings

    def _validate_delete(self, data: Dict[str, Any]) -> tuple:
        """Valida dados para DELETE"""
        errors = []
        warnings = []

        # ID é obrigatório
        if 'id' not in data or not data['id']:
            errors.append("Campo obrigatório faltando: id")

        # Valida ID
        if 'id' in data:
            try:
                conta_id = int(data['id'])
                if conta_id <= 0:
                    errors.append("id deve ser um número inteiro positivo")
            except (ValueError, TypeError):
                errors.append("id deve ser um número inteiro válido")

        return errors, warnings
