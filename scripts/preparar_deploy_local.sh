#!/bin/bash
# Script para preparar deploy local (Linux/Mac)
# Executa git add, commit e push

echo "============================================================"
echo "  PREPARANDO DEPLOY - AGENTE PESSOAL"
echo "============================================================"
echo ""

cd "$(dirname "$0")/.."

echo "Verificando status do Git..."
git status

echo ""
echo "Adicionando todos os arquivos..."
git add .

echo ""
echo "Criando commit..."
git commit -m "Deploy: Preparacao para servidor" || echo "Nenhuma mudanca para commitar"

echo ""
echo "Fazendo push para o repositorio..."
git push origin main || git push origin master

echo ""
echo "============================================================"
echo "  PREPARACAO CONCLUIDA!"
echo "============================================================"
echo ""
echo "Proximo passo:"
echo "  1. Conecte-se ao servidor: ssh root@srv1140258.hstgr.cloud"
echo "  2. Execute:"
echo "     cd /opt"
echo "     git clone git@github.com:wdsc1989/personal_agent.git"
echo "     cd personal_agent"
echo "     bash scripts/deploy_completo.sh"
echo ""
