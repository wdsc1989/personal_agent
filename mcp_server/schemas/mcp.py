"""
Schemas Pydantic para requisições e respostas MCP
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import date


class DetectRequest(BaseModel):
    """Request para detecção de intenção"""
    text: str = Field(..., description="Texto do usuário")
    context: Optional[Dict[str, Any]] = Field(None, description="Contexto adicional")


class DetectResponse(BaseModel):
    """Response da detecção de intenção"""
    action: str = Field(..., description="Ação detectada: INSERT, UPDATE, DELETE, LIST, REPORT, OTHER")
    entity: str = Field(..., description="Entidade: contas_pagar")
    confidence: float = Field(..., description="Confiança da detecção (0-1)")
    extracted_info: Optional[Dict[str, Any]] = Field(None, description="Informações extraídas básicas")


class ExtractRequest(BaseModel):
    """Request para extração de dados"""
    text: str = Field(..., description="Texto do usuário")
    action: str = Field(..., description="Ação: INSERT, UPDATE, DELETE, LIST")
    context: Optional[Dict[str, Any]] = Field(None, description="Contexto adicional")


class ExtractResponse(BaseModel):
    """Response da extração de dados"""
    data: Dict[str, Any] = Field(..., description="Dados extraídos estruturados")
    confidence: float = Field(..., description="Confiança da extração (0-1)")
    missing_fields: List[str] = Field(default_factory=list, description="Campos faltantes")


class ValidateRequest(BaseModel):
    """Request para validação de dados"""
    data: Dict[str, Any] = Field(..., description="Dados a validar")
    action: str = Field(..., description="Ação: INSERT, UPDATE, DELETE")


class ValidateResponse(BaseModel):
    """Response da validação"""
    valid: bool = Field(..., description="Se os dados são válidos")
    errors: List[str] = Field(default_factory=list, description="Lista de erros")
    warnings: List[str] = Field(default_factory=list, description="Lista de avisos")


class ListRequest(BaseModel):
    """Request para listagem de contas"""
    usuario_telegram_id: int = Field(..., description="ID do usuário no Telegram")
    data_inicial: Optional[date] = Field(None, description="Data inicial do período")
    data_final: Optional[date] = Field(None, description="Data final do período")
    status: Optional[str] = Field(None, description="Filtro por status")
    categoria: Optional[str] = Field(None, description="Filtro por categoria")


class ListResponse(BaseModel):
    """Response da listagem"""
    contas: List[Dict[str, Any]] = Field(..., description="Lista de contas")
    total: int = Field(..., description="Total de contas")
    total_valor: float = Field(..., description="Valor total das contas")


class FormatConfirmationRequest(BaseModel):
    """Request para formatação de confirmação"""
    action: str = Field(..., description="Ação: INSERT, UPDATE, DELETE")
    data: Dict[str, Any] = Field(..., description="Dados da ação")
    old_data: Optional[Dict[str, Any]] = Field(None, description="Dados antigos (para UPDATE)")


class FormatConfirmationResponse(BaseModel):
    """Response da formatação de confirmação"""
    message: str = Field(..., description="Mensagem formatada em Markdown")
    preview: Dict[str, Any] = Field(..., description="Preview dos dados")
