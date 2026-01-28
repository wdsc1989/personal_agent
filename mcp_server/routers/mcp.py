"""
Rotas MCP para detecção, extração, validação e listagem
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from datetime import date, datetime
import re

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.database import get_db_personal
from mcp_server.schemas.mcp import (
    DetectRequest, DetectResponse,
    ExtractRequest, ExtractResponse,
    ValidateRequest, ValidateResponse,
    ListRequest, ListResponse,
    FormatConfirmationRequest, FormatConfirmationResponse
)
from mcp_server.services.mcp_detector import MCPDetector
from mcp_server.services.mcp_extractor import MCPExtractor
from mcp_server.services.mcp_validator import MCPValidator
from mcp_server.services.mcp_lister import MCPLister
from mcp_server.services.mcp_formatter import MCPFormatter

router = APIRouter()


@router.post("/detect", response_model=DetectResponse)
async def detect_intention(
    request: DetectRequest,
    db: Session = Depends(get_db_personal)
):
    """
    Detecta a intenção do usuário a partir do texto
    """
    try:
        detector = MCPDetector(db)
        result = detector.detect(request.text, request.context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao detectar intenção: {str(e)}")


@router.post("/extract", response_model=ExtractResponse)
async def extract_data(
    request: ExtractRequest,
    db: Session = Depends(get_db_personal)
):
    """
    Extrai dados estruturados do texto
    """
    try:
        extractor = MCPExtractor(db)
        result = extractor.extract(request.text, request.action, request.context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao extrair dados: {str(e)}")


@router.post("/validate", response_model=ValidateResponse)
async def validate_data(
    request: ValidateRequest,
    db: Session = Depends(get_db_personal)
):
    """
    Valida dados antes de salvar
    """
    try:
        validator = MCPValidator(db)
        result = validator.validate(request.data, request.action)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao validar dados: {str(e)}")


@router.post("/list", response_model=ListResponse)
async def list_accounts(
    request: ListRequest,
    db: Session = Depends(get_db_personal)
):
    """
    Lista contas com filtros de período
    """
    try:
        lister = MCPLister(db)
        result = lister.list_accounts(
            request.usuario_telegram_id,
            request.data_inicial,
            request.data_final,
            request.status,
            request.categoria
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar contas: {str(e)}")


@router.post("/format-confirmation", response_model=FormatConfirmationResponse)
async def format_confirmation(
    request: FormatConfirmationRequest,
    db: Session = Depends(get_db_personal)
):
    """
    Formata mensagem de confirmação
    """
    try:
        formatter = MCPFormatter(db)
        result = formatter.format(request.action, request.data, request.old_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao formatar confirmação: {str(e)}")
