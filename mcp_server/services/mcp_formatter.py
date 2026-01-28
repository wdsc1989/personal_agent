"""
Serviço MCP para formatação de confirmações
"""
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from datetime import date

from mcp_server.schemas.mcp import FormatConfirmationResponse


class MCPFormatter:
    """
    Formata mensagens de confirmação
    """

    def __init__(self, db: Session):
        self.db = db

    def format(
        self,
        action: str,
        data: Dict[str, Any],
        old_data: Optional[Dict[str, Any]] = None
    ) -> FormatConfirmationResponse:
        """
        Formata mensagem de confirmação baseado na ação
        """
        if action == 'INSERT':
            return self._format_insert(data)
        elif action == 'UPDATE':
            return self._format_update(data, old_data)
        elif action == 'DELETE':
            return self._format_delete(data)
        else:
            return FormatConfirmationResponse(
                message="Ação não suportada",
                preview={}
            )

    def _format_insert(self, data: Dict[str, Any]) -> FormatConfirmationResponse:
        """Formata confirmação para INSERT"""
        message = "📝 **Nova Conta a Pagar**\n\n"
        message += "Confirme os dados antes de salvar:\n\n"
        
        preview = {}
        
        if 'nome_credor' in data:
            message += f"**Credor:** {data['nome_credor']}\n"
            preview['nome_credor'] = data['nome_credor']
        
        if 'valor_total' in data:
            valor = float(data['valor_total'])
            message += f"**Valor:** R$ {valor:,.2f}\n"
            preview['valor_total'] = valor
        
        if 'data_vencimento' in data:
            data_venc = data['data_vencimento']
            if isinstance(data_venc, str):
                data_obj = date.fromisoformat(data_venc)
            else:
                data_obj = data_venc
            message += f"**Vencimento:** {data_obj.strftime('%d/%m/%Y')}\n"
            preview['data_vencimento'] = data_obj.isoformat()
        
        if 'categoria' in data and data['categoria']:
            message += f"**Categoria:** {data['categoria']}\n"
            preview['categoria'] = data['categoria']
        
        if 'descricao' in data and data['descricao']:
            message += f"**Descrição:** {data['descricao']}\n"
            preview['descricao'] = data['descricao']
        
        if 'numero_parcelas' in data and data['numero_parcelas']:
            message += f"**Parcelas:** {data['numero_parcelas']}\n"
            preview['numero_parcelas'] = data['numero_parcelas']
        
        if 'parcela_atual' in data and data['parcela_atual']:
            message += f"**Parcela Atual:** {data['parcela_atual']}\n"
            preview['parcela_atual'] = data['parcela_atual']
        
        message += "\n✅ Responda **SIM** para confirmar\n"
        message += "❌ Responda **NÃO** para cancelar"
        
        return FormatConfirmationResponse(
            message=message,
            preview=preview
        )

    def _format_update(
        self,
        data: Dict[str, Any],
        old_data: Optional[Dict[str, Any]] = None
    ) -> FormatConfirmationResponse:
        """Formata confirmação para UPDATE"""
        message = "✏️ **Atualizar Conta a Pagar**\n\n"
        message += "Confirme as alterações:\n\n"
        
        preview = {'id': data.get('id')}
        
        if old_data:
            message += "**Antes:**\n"
            if 'nome_credor' in old_data:
                message += f"- Credor: {old_data['nome_credor']}\n"
            if 'valor_total' in old_data:
                message += f"- Valor: R$ {float(old_data['valor_total']):,.2f}\n"
            if 'data_vencimento' in old_data:
                message += f"- Vencimento: {old_data['data_vencimento']}\n"
            message += "\n**Depois:**\n"
        
        if 'nome_credor' in data:
            message += f"- Credor: {data['nome_credor']}\n"
            preview['nome_credor'] = data['nome_credor']
        
        if 'valor_total' in data:
            valor = float(data['valor_total'])
            message += f"- Valor: R$ {valor:,.2f}\n"
            preview['valor_total'] = valor
        
        if 'data_vencimento' in data:
            data_venc = data['data_vencimento']
            if isinstance(data_venc, str):
                data_obj = date.fromisoformat(data_venc)
            else:
                data_obj = data_venc
            message += f"- Vencimento: {data_obj.strftime('%d/%m/%Y')}\n"
            preview['data_vencimento'] = data_obj.isoformat()
        
        if 'status' in data:
            message += f"- Status: {data['status']}\n"
            preview['status'] = data['status']
        
        message += "\n✅ Responda **SIM** para confirmar\n"
        message += "❌ Responda **NÃO** para cancelar"
        
        return FormatConfirmationResponse(
            message=message,
            preview=preview
        )

    def _format_delete(self, data: Dict[str, Any]) -> FormatConfirmationResponse:
        """Formata confirmação para DELETE"""
        message = "🗑️ **Excluir Conta a Pagar**\n\n"
        message += "⚠️ Atenção: Esta ação não pode ser desfeita!\n\n"
        
        preview = {'id': data.get('id')}
        
        if 'id' in data:
            message += f"**ID da Conta:** {data['id']}\n"
        
        message += "\n✅ Responda **SIM** para confirmar a exclusão\n"
        message += "❌ Responda **NÃO** para cancelar"
        
        return FormatConfirmationResponse(
            message=message,
            preview=preview
        )
